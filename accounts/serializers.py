from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import CustomUser

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "name",
            "image",
            "is_active",
            "is_superuser",
        ]
        read_only_fields = ["is_active", "is_superuser"]


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "name", "image", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            name=validated_data["name"],
            image=validated_data["image"],
            password=validated_data["password"],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "name",
            "image",
        ]
