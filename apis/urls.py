from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    LevelViewSet,
    RiddleViewSet,
    LeaderboardViewSet,
    CurrentLevelViewSet,
    UserProfileView,
)

router = DefaultRouter()

router.register(r"levels", LevelViewSet, basename="level")
router.register(r"riddles", RiddleViewSet, basename="riddle")
router.register(r"leaderboard", LeaderboardViewSet, basename="leaderboard")
router.register(r"current-level", CurrentLevelViewSet, basename="current-level")


urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("", include(router.urls)),
]
