from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django.db.models import Count


from rest_framework.permissions import IsAuthenticated

from apis.models import *


from apis.serializers import *
from .permissions import IsSuperUserOrReadOnly


class LevelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    def retrieve(self, request, *args, **kwargs):
        level_id = kwargs.get("pk")
        queryset = self.queryset.filter(number=level_id)
        level = queryset.first()
        if level is None:
            raise NotFound(detail=f"Level with number {level_id} not found.")
        serializer = self.get_serializer(level)
        return Response(serializer.data)


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

    def retrieve(self, request, *args, **kwargs):
        riddle_id = kwargs.get("pk")
        queryset = self.queryset.filter(riddle_id=riddle_id)
        riddle = queryset.first()
        if riddle is None:
            raise NotFound(detail=f"Riddle with riddle_id {riddle_id} not found.")
        serializer = self.get_serializer(riddle)
        return Response(serializer.data)

    # Verify the answer of the riddle
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def verify(self, request, pk=None):
        riddle = self.retrieve(request, pk=pk).data
        user = request.user
        answer = request.data.get("answer")

        if answer is None:
            return Response(
                {"error": "Answer is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if riddle["answer"].lower().strip() == answer.lower().strip():
            if riddle["is_trap"] == True:
                # Check if the user has already submitted this trap riddle
                if not UserTrapSubmission.objects.filter(
                    user=user, level_id=riddle["level"], riddle_id=riddle["riddle_id"]
                ).exists():
                    UserTrapSubmission.objects.create(
                        user=user,
                        level_id=riddle["level"],
                        riddle_id=riddle["riddle_id"],
                    )
                return Response({"result": "correct", "trap": True})
            # correct answer and not a trap
            # update the user's current level
            progress = Leaderboard.objects.get(team_id=user.id)
            progress.current_level = riddle["level"]
            progress.save()
            return Response({"result": "correct", "trap": False})
        else:
            return Response({"result": "incorrect", "trap": riddle["is_trap"]})


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


# class UserRiddleAttemptViewSet(viewsets.ModelViewSet):
#     queryset = UserRiddleAttempt.objects.all()
#     serializer_class = UserRiddleAttemptSerializer

#     @action(detail=False, methods=["post"])
#     def submit_answer(self, request):
#         user = request.user
#         riddle_id = request.data.get("riddle_id")
#         answer = request.data.get("answer")

#         riddle = Riddle.objects.get(id=riddle_id)
#         is_correct = riddle.answer == answer
#         is_trap = riddle.is_trap

#         attempt = UserRiddleAttempt.objects.create(
#             user=user, riddle=riddle, is_correct=is_correct, is_trap=is_trap
#         )

#         if is_correct:
#             user.score += 10
#             user.save()

#         return Response(UserRiddleAttemptSerializer(attempt).data)
