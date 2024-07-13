from rest_framework import serializers
from apis.models import Level


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"
