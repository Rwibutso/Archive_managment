from pyexpat import model
from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
UserModel = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(User.objects.all(), "Email exists!")
                ],
            },
        }


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")



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
            # "phone",
            "password",
            # "user_type",
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
            # "phone",
            "password",
            # "user_type",
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
            # "phone",
            # "user_type",
        )