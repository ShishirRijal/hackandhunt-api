from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, name, image, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        if not username:
            raise ValueError("Username is required.")
        if not name:
            raise ValueError("Name is required.")
        if not image:
            raise ValueError("Image is required.")
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, image=image, name=name, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, username, email, name, image, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, email, name, image, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    name = models.CharField(max_length=50)
    image = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name", "image"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
