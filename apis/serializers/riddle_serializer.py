from rest_framework import serializers
from apis.models.riddle import Riddle


class RiddleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riddle
        fields = "__all__"
        read_only_fields = ["id"]


class RiddleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riddle
        fields = "__all__"
        read_only_fields = ["riddle_id", "id", "level"]
