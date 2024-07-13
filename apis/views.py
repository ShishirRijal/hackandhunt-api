from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Window
from django.db.models.functions import RowNumber


from apis.models import *


from apis.serializers import *
from .permissions import IsSuperUserOrReadOnly


class LevelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class RiddleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Riddle.objects.all()
    serializer_class = RiddleSerializer

    # Get riddles according to the level_id
    def get_queryset(self):
        level_id = self.request.query_params.get("level_id")
        if level_id is not None:
            # Filter by level_id if provided
            return Riddle.objects.filter(level_id=level_id)
        else:
            # Otherwise, return all riddles
            return Riddle.objects.all()


class LeaderboardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        return Leaderboard.objects.annotate(
            rank=Window(
                expression=RowNumber(),
                order_by=[F("current_level").desc(), F("updated_at").asc()],
            )
        )


class CurrentLevelViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Get the current user's TeamProgress
        try:
            progress = Leaderboard.objects.get(team_id=request.user.id)
            serializer = UserCurrentLevelSerializer(progress)
            print(f"sera: {(serializer.data)['current_level']}")
            return Response(serializer.data)
        except Leaderboard.DoesNotExist:
            return Response({"detail": "Team progress not found."}, status=404)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
