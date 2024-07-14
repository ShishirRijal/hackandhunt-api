from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTrapSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level_id = models.IntegerField(null=False)
    riddle_id = models.CharField(max_length=10, null=False)
    submission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "level_id", "riddle_id")

    def __str__(self):
        return f"User {self.user.id} - Level {self.level_id} - Riddle {self.riddle_id}"
