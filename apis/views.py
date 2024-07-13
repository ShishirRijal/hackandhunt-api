from django.shortcuts import render
from rest_framework import viewsets

from apis.models.level import Level
from apis.serializers.level_serializer import LevelSerializer
from .permissions import IsSuperUserOrReadOnly


class LevelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
