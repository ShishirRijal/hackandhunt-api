from rest_framework.routers import DefaultRouter
from .views import LevelViewSet, RiddleViewSet

router = DefaultRouter()

router.register(r"levels", LevelViewSet, basename="level")
router.register(r"riddles", RiddleViewSet, basename="riddle")

urlpatterns = router.urls
