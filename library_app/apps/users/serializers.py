from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from library_app.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )
        read_only_fields = ("username",)


class CreateUserSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    @staticmethod
    def create(validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "tokens",
        )
        read_only_fields = ("auth_token",)
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def get_tokens(obj: User):
        refresh = RefreshToken.for_user(obj)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
