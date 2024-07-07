from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "name", "is_active", "is_superuser"]
        read_only_fields = ["is_active", "is_superuser"]
