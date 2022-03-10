from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from users.utils.password_validator import is_password_valid
from dj_rest_auth.serializers import LoginSerializer


UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        style={"input_type": "first_name"}, write_only=True
    )
    last_name = serializers.CharField(
        style={"input_type": "last_name"}, write_only=True
    )
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = UserModel
        fields = ["first_name", "last_name", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, request):
        user = UserModel(email=self.validated_data["email"])
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        username = self.validated_data["email"]

        if not is_password_valid(self.validated_data["password"]):
            raise serializers.ValidationError(
                {
                    "detail": _(
                        "The password must contain at least 1 uppercase letter, 1 special character and a minimum length of 8 characters"
                    )
                }
            )

        if password != password2:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.save()
        return user


class LoginSerializer(LoginSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = UserModel
        fields = ["email", "password"]
        extra_kwargs = {"username": {"read_only": True}}


class UserAddSerializer(serializers.ModelSerializer):
    """
    A User serializer to render for User updates
    """

    class Meta:
        model = UserModel
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
        )


class UserEditSerializer(serializers.ModelSerializer):
    """
    A User serializer to render for User updates
    """

    class Meta:
        model = UserModel
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
    
        )


class UserViewSerializer(serializers.ModelSerializer):
    """
    A User serializer to render for User updates
    """

    class Meta:
        model = UserModel
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            
        )
