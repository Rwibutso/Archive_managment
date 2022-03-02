from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from users.serializers import *
from rest_framework import status, filters
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from django_filters.rest_framework import DjangoFilterBackend


class UserDetailsView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserViewSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = [u"get"]

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
            current_profile = current_user.profile

            user_serialized = self.serializer_class(
                current_user, context={"request": request}
            ).data

            # ----------------------- default Settings----------------------------------
            try:
                # Get the user's default Country
                if current_profile.country is None:
                    ip_address = get_ip(request)
                    g = GeoIP2()
                    country_code = str(g.country_code(ip_address))
                    country = Country.objects.get(iso_2=country_code)
                    current_profile.country = country
                    current_profile.save()

                # Get the user's default Language
                if current_profile.language is None:
                    meta = str(request.META.get("HTTP_ACCEPT_LANGUAGE"))
                    language_meta_split = meta.split(";")
                    language_first_element = language_meta_split[0].split(",")[0]
                    try:
                        language = Language.objects.get(iso_2=language_first_element)
                    except Language.DoesNotExist:
                        language_first_element = (
                            language_meta_split[0].split(",")[0].split("-")[0]
                        )
                        language = Language.objects.get(iso_2=language_first_element)
                    current_user.language = language
                    current_profile.save()

                # Get the user's default Currency
                if current_profile.currency is None:
                    ip_address = get_ip(request)
                    g = GeoIP2()
                    country_code = str(g.country_code(ip_address))
                    country = Country.objects.get(iso_2=country_code)
                    currency = Currency.objects.get(
                        currency_label=country.currency_code
                    )
                    current_profile.currency = currency
                    current_profile.save()
            except Exception:
                pass

            return Response(user_serialized)
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": _("User is not registered")},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserViewSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = [u"get", u"put", u"delete"]

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
                    if not is_password_valid(request.data["password"]):
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


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserViewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    http_method_names = [u"get", u"post"]

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

    # def post(self, request, *args, **kwargs):
    #     try:
    #         serializer = UserAddSerializer(data=request.data)

    #         if not serializer.is_valid():
    #             data_errors = {}
    #             data_message = str("")
    #             for P, M in serializer.errors.items():
    #                 data_message += P + ": " + M[0].replace(".", "") + ", "
    #             data_errors["detail"] = data_message
    #             return Response(data_errors, status=status.HTTP_400_BAD_REQUEST)
    #         try:
    #             groups_data = serializer.validated_data.pop("groups")
    #         except Exception:
    #             groups_data = list()

    #         user = get_user_model()(
    #             username=serializer.validated_data["username"],
    #             email=serializer.validated_data["username"],
    #             first_name=serializer.validated_data["first_name"],
    #             last_name=serializer.validated_data["last_name"],
    #             # phone=serializer.validated_data["phone"],
    #         )
    #         try:
    #             user_type = serializer.validated_data["user_type"].upper()
    #         except Exception:
    #             user_type = "CLIENT"

    #         try:
    #             is_super_controller = self.validated_data["is_super_controller"]
    #         except Exception:
    #             is_super_controller = False

    #         try:
    #             is_super_technician = self.validated_data["is_super_technician"]
    #         except Exception:
    #             is_super_technician = False

    #         is_staff = False
    #         if user_type == "STAFF":
    #             is_staff = True

    #         if not is_password_valid(serializer.validated_data["password"]):
    #             raise serializers.ValidationError(
    #                 {
    #                     "detail": _(
    #                         "The password must contain at least 1 uppercase letter, 1 special character and a minimum length of 8 characters"
    #                     )
    #                 }
    #             )

    #         password = serializer.validated_data["password"]
    #         user.set_password(password)
    #         user.user_type = user_type.upper()
    #         user.is_staff = is_staff
    #         user.is_super_controller = is_super_controller
    #         user.is_super_technician = is_super_technician
    #         user.is_active = True
    #         user.sub_user_id = request.user
    #         user.save()

    #         EmailAddress.objects.create(
    #             user=user, email=user.email, verified=True, primary=True
    #         )
    #         Profile.objects.create(user=user)

    #         if len(groups_data) != 0:
    #             for group_data in groups_data:
    #                 user.groups.add(group_data)

    #         # Add the new user to the STAFF group
    #         if is_staff:
    #             group, _created = Group.objects.get_or_create(
    #                 name=user_type.capitalize()
    #             )
    #             user.groups.add(group)

    #         serializer_data = UserViewSerializer(user).data
    #         return Response(serializer_data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        Returns a list all users
        """
        # queryset = self.get_queryset()
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)