from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "id", "name", "email", "is_active", "is_superuser"]

    # Define fieldsets for editing existing users in the admin panel
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": ("name", "image"),
            },
        ),
    )

    # Define fieldsets for adding new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": ("name", "email", "image", "is_active", "is_superuser"),
            },
        ),
    )


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
