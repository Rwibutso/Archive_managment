import imp
from lib2to3.pgen2 import token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from users.serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from knox import views as knox_views
from rest_framework.views import APIView




# @api_view(["POST"])
# def login_api(request):
#     serializer = AuthTokenSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.validated_data["user"]
#     __, token = AuthToken.objects.create(user)

#     return Response(
#         {
#             "user_info": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#             },
#             "token": token,
#         }
#     )


class LoginVieww(APIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ["post"]

    # def post(self, request, *args, **kwargs):
    #     """
    #     This endpoint lets a user add comments on a course.
    #     """

    #     # try:
    #     serializer = self.serializer_class(data=request.data)
    #     if not serializer.is_valid():
    #         data_errors = {}
    #         data_message = str("")
    #         for P, M in serializer.errors.items():
    #             data_message += P + ": " + M[0].replace(".", "") + ", "
    #         data_errors["detail"] = data_message
    #         return Response(data_errors, status=status.HTTP_201_CREATED)

    #     user = serializer.validated_data["user"]
    #     __, token = AuthToken.objects.create(user)

    #     user_info = {
    #         "id": user.id,
    #         "username": user.username,
    #         "email": user.email,
    #         # "token": token,
    #     }
    #     return Response(
    #         {"detail": "You are logged in!", "data": user_info},
    #         status=status.HTTP_200_OK,
    #     )
    #     # except Exception as e:
    #     #     return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import DateTimeField
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import knox_settings
from rest_framework.generics import GenericAPIView
class LoginView(GenericAPIView):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    http_method_names = ["post"]

    def get_context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def get_user_serializer_class(self):
        return self.serializer_class

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()
        print(self.get_user_serializer_class())
        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data

    def post(self, request, *args, **kwargs):
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"detail": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)
        return Response(data)



@api_view(["GET"])
def get_user_data(request):
    user = request.user

    if user.is_authenticated:
        return Response(
            {
                "user_info": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            }
        )

    return Response({"error": "You are not authanticated!"}, status=400)


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        """
        This endpoint lets a user add comments on a course.
        """

        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                data_errors = {}
                data_message = str("")
                for P, M in serializer.errors.items():
                    data_message += P + ": " + M[0].replace(".", "") + ", "
                data_errors["detail"] = data_message
                return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            __, token = AuthToken.objects.create(user)

            user_info = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "token": token,
            }
            return Response(
                {"detail": "user successfully registered", "data": user_info},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



# class EditView(generics.RetrieveUpdateAPIView):
#     queryset = get_user_model.objects.all()
#     serializer_class = UserEditSerializer
#     permission_classes = (IsAuthenticated,)
#     http_method_names = [u"put"]

#     def put(self, request, *args, **kwargs):
#         """
#         Updates user's detailed information
#         """
#         try:
#             current_user = get_user_model().objects.get(id=kwargs["pk"])
#             if "password" in request.data:
#                 if (
#                     len(request.data["password"]) < 1
#                     or request.data["password"] == "undefined"
#                 ):
#                     pass
#                 else:
#                     if not is_password_valid(request.data["password"]):
#                         return Response(
#                             {
#                                 "detail": _(
#                                     "The password must contain at least 1 uppercase letter, 1 special character and a minimum length of 8 characters"
#                                 )
#                             },
#                             status=status.HTTP_400_BAD_REQUEST,
#                         )
#                     current_user.set_password(request.data["password"])
#                     current_user.save()

#             data = request.data.copy()
#             try:
#                 data.pop("password")
#             except KeyError:
#                 pass
#             partial = kwargs.pop("partial", True)
#             serializer = self.get_serializer(current_user, data=data, partial=partial)

#             if not serializer.is_valid():
#                 data_errors = {}
#                 data_message = str("")
#                 for P, M in serializer.errors.items():
#                     data_message += P + ": " + M[0].replace(".", "") + ", "
#                 data_errors["detail"] = data_message
#                 return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)

#             self.perform_update(serializer)
#             user_serialized = UserEditSerializer(current_user).data
#             return Response(user_serialized)
#         except get_user_model().DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)