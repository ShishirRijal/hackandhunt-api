# Generated by Django 5.0.6 on 2024-07-15 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_customuser_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="image",
            field=models.TextField(blank=True, null=True),
        ),
    ]
