from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apis.models import Leaderboard


# Create TeamProgress for every new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_team_progress(sender, instance, created, **kwargs):
    if created:
        Leaderboard.objects.create(team_id=instance)
