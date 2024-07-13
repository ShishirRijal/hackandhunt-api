from rest_framework import serializers
from apis.models.riddle import Riddle


class RiddleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riddle
        fields = "__all__"
