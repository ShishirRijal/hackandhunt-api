from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django.shortcuts import get_object_or_404


from rest_framework.permissions import IsAuthenticated

from apis.models import *


from apis.serializers import *
from .permissions import IsSuperUserOrReadOnly


class LevelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     level_id = kwargs.get("pk")
    #     queryset = self.queryset.filter(id=level_id)
    #     level = queryset.first()
    #     if level is None:
    #         raise NotFound(detail=f"Level with number {level_id} not found.")
    #     serializer = self.get_serializer(level)
    #     return Response(serializer.data)


class RiddleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Riddle.objects.all()
    serializer_class = RiddleSerializer

    # update the POST method to link level number to level_id
    def create(self, request, *args, **kwargs):
        data = request.data
        level_number = data.get("level")
        level = Level.objects.get(number=level_number)
        data["level"] = level.number
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # print(f"serializer: {serializer.data}")
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = RiddleUpdateSerializer
        return super().partial_update(request, *args, **kwargs)

    # def partial_update(self, request, *args, **kwargs):
    #     riddle_id = kwargs.get("pk")
    #     print(f"riddle_id: {riddle_id}")
    #     queryset = self.queryset.filter(id=riddle_id)
    #     print(f"queryset: {queryset}")
    #     riddle = queryset.first()
    #     print(f"riddle: {riddle}")
    #     if riddle is None:
    #         raise NotFound(detail=f"Riddle with riddle_id {riddle_id} not found.")
    #     serializer = self.get_serializer(riddle, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    # Get riddles according to the level_id
    def get_queryset(self):
        user = self.request.user
        level_id = self.request.query_params.get("level")

        if level_id is None:
            return self.queryset.all()
        else:
            if not user.is_superuser:
                # Check if user is currently on this specific level
                progress = Leaderboard.objects.get(team_id=user.id)
                if progress.current_level < int(level_id) - 1:
                    raise PermissionDenied(
                        detail=f"Cannot access riddles for level {level_id}."
                    )
            N = 3  # Number of submissions required to lock all trap riddles
            # Get all riddles for the given level
            riddles = Riddle.objects.filter(level=level_id)

            # Find the riddle IDs that have more than 5 submissions for the current user and level
            trap_submissions = UserTrapSubmission.objects.filter(
                user=user, level_id=level_id
            ).count()

            # If the user has submitted more than N trap riddles, return only non-trap riddles
            if trap_submissions > N:
                return riddles.filter(is_trap=False)
            # else, return all riddles
            else:
                return riddles.all()

    def retrieve(self, request, *args, **kwargs):
        riddle_id = kwargs.get("pk")
        queryset = self.queryset.filter(id=riddle_id)
        riddle = queryset.first()
        if riddle is None:
            raise NotFound(detail=f"Riddle with id {riddle_id} not found.")
        # Check if user is currently on this specific level
        user = request.user
        if not user.is_superuser:
            progress = Leaderboard.objects.get(team_id=user.id)
            if progress.current_level < riddle.level.number - 1:
                raise PermissionDenied(
                    detail=f"Cannot access riddle from level {riddle.level.number}."
                )
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
