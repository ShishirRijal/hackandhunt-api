# Generated by Django 5.0.6 on 2024-07-13 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apis", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="level",
            name="image",
            field=models.TextField(null=True),
        ),
    ]
