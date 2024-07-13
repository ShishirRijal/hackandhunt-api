from django.db import models


class Level(models.Model):
    number = models.IntegerField(null=False, unique=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()
    image = models.TextField(null=True)

    def __str__(self):
        return f"Level {self.number}: {self.name}"
