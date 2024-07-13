from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Leaderboard(models.Model):
    team_id = models.ForeignKey(User, on_delete=models.CASCADE)
    current_level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Team {self.team_id}: Level {self.current_level}"
