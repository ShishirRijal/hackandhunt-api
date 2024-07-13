from rest_framework import serializers
from apis.models import Leaderboard


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = "__all__"


class UserCurrentLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ["current_level"]
