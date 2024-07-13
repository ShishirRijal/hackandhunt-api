from rest_framework.routers import DefaultRouter
from .views import LevelViewSet, RiddleViewSet, LeaderboardViewSet, CurrentLevelViewSet

router = DefaultRouter()

router.register(r"levels", LevelViewSet, basename="level")
router.register(r"riddles", RiddleViewSet, basename="riddle")
router.register(r"leaderboard", LeaderboardViewSet, basename="leaderboard")

urlpatterns = router.urls
