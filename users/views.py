from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status, filters
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.serializers import VerifyEmailSerializer
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import (
    UserViewSerializer,
    UserEditSerializer,
    UserAddSerializer,
    RegisterSerializer,
)
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup
from dj_rest_auth.app_settings import JWTSerializer, TokenSerializer, create_token
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from dj_rest_auth.registration.app_settings import register_permission_classes
from dj_rest_auth.app_settings import (
    JWTSerializer,
    LoginSerializer,
    TokenSerializer,
    create_token,
)
from django.db.models.functions import Lower

# from users.serializers import *
from django.contrib.auth import login as django_login
from rest_framework.generics import GenericAPIView
from django.contrib.auth import logout as django_logout
from dj_rest_auth.app_settings import (
    PasswordResetSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
)
from dj_rest_auth.models import TokenModel
from dj_rest_auth.utils import jwt_encode

# from django.contrib.auth.password_validation import is_password_valid

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("password1", "password2")
)
UserModel = get_user_model()


######################### Register ##########################
class SignupView(CreateAPIView):
    """
    Creates a new user instance. Accept the following POST parameters:
    first_name, last_name, email, password, password2)
    And a Confirmation Email is sent to the New created User.
    """

    serializer_class = RegisterSerializer
    queryset = get_user_model().objects.all()
    permission_classes = register_permission_classes()
    token_model = TokenModel
    throttle_scope = "dj_rest_auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(SignupView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if (
            allauth_settings.EMAIL_VERIFICATION
            == allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, "REST_USE_JWT", False):
            data = {
                "user": user,
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
            }
            return JWTSerializer(data, context=self.get_serializer_context()).data
        else:
            return TokenSerializer(
                user.auth_token, context=self.get_serializer_context()
            ).data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if (
            allauth_settings.EMAIL_VERIFICATION
            != allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            if getattr(settings, "REST_USE_JWT", False):
                self.access_token, self.refresh_token = jwt_encode(user)
            else:
                create_token(self.token_model, user, serializer)

        complete_signup(
            self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None
        )
        user.is_active = False
        user.save()
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            data_errors = {}
            data_message = str("")
            for P, M in serializer.errors.items():
                data_message += P + ": " + M[0].replace(".", "") + ", "
            data_errors["detail"] = data_message
            return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        self.get_success_headers(serializer.data)
        return Response(
            {
                "detail": _(
                    "Registration successfully completed. Please check your email to activate your account"
                )
            },
            status=status.HTTP_201_CREATED,
        )


################### Email Confirmation ##############
class VerifyEmailView(APIView, ConfirmEmailView):
    """
    Confirms a user's email address
    Accept the following POST parameters: code key
    Note that the User is not automatically logged in!
    Example: http://localhost:800/account/email/verification/
    data: {
    "key": "Ng:1nPqJO:tlHVspnG4MIFCaWQrf9U2gohhyqwwB91e72clbWyXas"
            }
    """

    permission_classes = (AllowAny,)
    allowed_methods = ("POST", "OPTIONS", "HEAD")

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response(
            {"detail": _("You have successfully confirmed your Email")},
            status=status.HTTP_200_OK,
        )


############### Login################
class LoginView(GenericAPIView):
    """
    Check the credentials and returns an access Token Object
    if the credentials are valid and authenticated.
    Accept the following POST parameters: email, password,
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel
    throttle_scope = "dj_rest_auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, "REST_USE_JWT", False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):

        self.user = self.serializer.validated_data["user"]
        # for JWT Auth Pair Tokens
        if getattr(settings, "REST_USE_JWT", False):
            self.access_token, self.refresh_token = jwt_encode(self.user)

        # for Simple REST Auth Token
        else:
            self.token = create_token(self.token_model, self.user, self.serializer)

        if getattr(settings, "REST_SESSION_LOGIN", True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()
        access_token_expiration = None
        refresh_token_expiration = None
        if getattr(settings, "REST_USE_JWT", False):
            from rest_framework_simplejwt.settings import api_settings as jwt_settings

            access_token_expiration = (
                timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
            )
            refresh_token_expiration = (
                timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
            )
            return_expiration_times = getattr(
                settings, "JWT_AUTH_RETURN_EXPIRATION", False
            )

            data = {
                "user": self.user,
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
            }

            serializer = serializer_class(
                instance=data, context=self.get_serializer_context()
            )
        else:
            serializer = serializer_class(
                instance=self.token, context=self.get_serializer_context()
            )

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, "REST_USE_JWT", False):
            cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
            refresh_cookie_name = getattr(settings, "JWT_AUTH_REFRESH_COOKIE", None)
            refresh_cookie_path = getattr(settings, "JWT_AUTH_REFRESH_COOKIE_PATH", "/")
            cookie_secure = getattr(settings, "JWT_AUTH_SECURE", False)
            cookie_httponly = getattr(settings, "JWT_AUTH_HTTPONLY", True)
            cookie_samesite = getattr(settings, "JWT_AUTH_SAMESITE", "Lax")

            if cookie_name:
                response.set_cookie(
                    cookie_name,
                    self.access_token,
                    expires=access_token_expiration,
                    secure=cookie_secure,
                    httponly=cookie_httponly,
                    samesite=cookie_samesite,
                )

            if refresh_cookie_name:
                response.set_cookie(
                    refresh_cookie_name,
                    self.refresh_token,
                    expires=refresh_token_expiration,
                    secure=cookie_secure,
                    httponly=cookie_httponly,
                    samesite=cookie_samesite,
                    path=refresh_cookie_path,
                )
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid():
            data_errors = {}
            data_message = str("")
            for P, M in self.serializer.errors.items():
                data_message += P + ": " + M[0].replace(".", "") + ", "
            data_errors["detail"] = data_message
            return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

        self.login()
        return self.get_response()


############### Logout #################


class LogoutView(APIView):
    """
    Once called, it expires the Token object
    assigned to the current User object.
    """

    permission_classes = (AllowAny,)
    throttle_scope = "dj_rest_auth"

    def get(self, request, *args, **kwargs):
        if getattr(settings, "ACCOUNT_LOGOUT_ON_GET", False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        if getattr(settings, "REST_SESSION_LOGIN", True):
            django_logout(request)

        response = Response(
            {"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK
        )

        if getattr(settings, "REST_USE_JWT", False):
            # NOTE: this import occurs here rather than at the top level
            # because JWT support is optional, and if `REST_USE_JWT` isn't
            # True we shouldn't need the dependency
            from rest_framework_simplejwt.exceptions import TokenError
            from rest_framework_simplejwt.tokens import RefreshToken

            cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
            if cookie_name:
                response.delete_cookie(cookie_name)
            refresh_cookie_name = getattr(settings, "JWT_AUTH_REFRESH_COOKIE", None)
            if refresh_cookie_name:
                response.delete_cookie(refresh_cookie_name)

            if "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS:
                # add refresh token to blacklist
                try:
                    token = RefreshToken(request.data["refresh"])
                    token.blacklist()
                except KeyError:
                    response.data = {
                        "detail": _("Refresh token was not included in request data.")
                    }
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                except (TokenError, AttributeError, TypeError) as error:
                    if hasattr(error, "args"):
                        if (
                            "Token is blacklisted" in error.args
                            or "Token is invalid or expired" in error.args
                        ):
                            response.data = {"detail": _(error.args[0])}
                            response.status_code = status.HTTP_401_UNAUTHORIZED
                        else:
                            response.data = {"detail": _("An error has occurred.")}
                            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

                    else:
                        response.data = {"detail": _("An error has occurred.")}
                        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            else:
                message = _(
                    "Neither cookies or blacklist are enabled, so the token "
                    "has not been deleted server side. Please make sure the token is deleted client side."
                )
                response.data = {"detail": message}
                response.status_code = status.HTTP_200_OK
        return response


############ Password Reset ######################3


class PasswordResetView(GenericAPIView):
    """
    Accepts the following POST parameters: email
    and sends email with password reset link
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "dj_rest_auth"

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            data_errors = {}
            data_message = str("")
            for P, M in serializer.errors.items():
                data_message += P + ": " + M[0].replace(".", "") + ", "
            data_errors["detail"] = data_message
            return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

        if not UserModel.objects.annotate(
            email_lower=Lower("email".replace(" ", ""))
        ).filter(email_lower=request.data["email"].lower().replace(" ", "")):

            return Response(
                {"detail": _("There is no account registered with your email address")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            serializer.save()
            # Return the success message with OK HTTP status
            return Response(
                {"detail": _("Password reset e-mail has been sent.")},
                status=status.HTTP_200_OK,
            )


############ Password Change ################


class PasswordChangeView(GenericAPIView):
    """
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    throttle_scope = "dj_rest_auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            data_errors = {}
            data_message = str("")
            for P, M in serializer.errors.items():
                data_message += P + ": " + M[0].replace(".", "") + ", "
            data_errors["detail"] = data_message
            return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})


################ Password Reset Confirm ####################33


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    Accepts the following POST parameters: token, uid,
    new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "dj_rest_auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            data_errors = {}
            data_message = str("")
            for P, M in serializer.errors.items():
                data_message += P + ": " + M[0].replace(".", "") + ", "
            data_errors["detail"] = data_message
            return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"detail": _("Password has been reset with the new password.")})


############# User Me #####################


class UserDetailsView(generics.RetrieveAPIView):
    """
    Returns my(me connected user) profile details

    """

    queryset = get_user_model().objects.all()
    serializer_class = UserViewSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes
        called when using django-rest-swagger
        """
        return get_user_model().objects.none()

    def get(self, request, *args, **kwargs):
        """
        Returns connected user's detailed informations
        """
        try:
            current_user = get_user_model().objects.get(email=request.user.email)
            user_serialized = self.serializer_class(
                current_user, context={"request": request}
            ).data

            return Response(user_serialized)
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": _("User is not registered")},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserViewSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "put", "delete"]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UserEditSerializer
        return UserViewSerializer

    def get(self, request, *args, **kwargs):
        """
        Returns user's detailed informations
        """
        try:
            current_user = get_user_model().objects.get(id=kwargs["pk"])
            user_serialized = UserViewSerializer(current_user).data
            return Response(user_serialized)
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": _("User is not registered")},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, *args, **kwargs):
        """
        Updates user's detailed information
        """
        try:
            current_user = get_user_model().objects.get(id=kwargs["pk"])
            if "password" in request.data:
                if (
                    len(request.data["password"]) < 1
                    or request.data["password"] == "undefined"
                ):
                    pass
                else:
                    if not (request.data["password"]):
                        return Response(
                            {
                                "detail": _(
                                    "The password must contain at least 1 uppercase letter, 1 special character and a minimum length of 8 characters"
                                )
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    current_user.set_password(request.data["password"])
                    current_user.save()

            data = request.data.copy()
            try:
                data.pop("password")
            except KeyError:
                pass
            partial = kwargs.pop("partial", True)
            serializer = self.get_serializer(current_user, data=data, partial=partial)

            if not serializer.is_valid():
                data_errors = {}
                data_message = str("")
                for P, M in serializer.errors.items():
                    data_message += P + ": " + M[0].replace(".", "") + ", "
                data_errors["detail"] = data_message
                return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

            self.perform_update(serializer)
            user_serialized = UserViewSerializer(current_user).data
            return Response(user_serialized)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        """
        Removes a user from the database
        """
        try:
            current_user = get_user_model().objects.get(id=kwargs["pk"])
            current_user.delete()
            return Response(
                {"detail": _("User successfully deleted")}, status=status.HTTP_200_OK
            )
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserListView(generics.ListAPIView):
    """
    Returns a list of all users

    """

    serializer_class = UserViewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserAddSerializer
        return UserViewSerializer

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ["email", "last_name", "first_name"]
    search_fields = ["=username", "=email", "^last_name", "^first_name"]
    ordering_fields = ["date_joined", "last_login"]

    def get(self, request, *args, **kwargs):
        """
        Returns a list all users
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
