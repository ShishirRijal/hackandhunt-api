from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username
