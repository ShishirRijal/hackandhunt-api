# Generated by Django 5.0.6 on 2024-07-13 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apis", "0004_remove_riddle_number_riddle_riddle_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="riddle",
            name="link",
            field=models.TextField(null=True),
        ),
    ]
