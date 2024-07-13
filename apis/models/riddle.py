from django.db import models


class Riddle(models.Model):
    number = models.IntegerField(null=False, unique=True)
    question = models.TextField(null=False)
    answer = models.CharField(null=False, max_length=255)
    level = models.ForeignKey("Level", on_delete=models.CASCADE)
    is_trap = models.BooleanField(default=False)
    code = models.TextField(null=True)
    image = models.TextField(null=True)
    hint = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Riddle {self.number}: {self.question}"
