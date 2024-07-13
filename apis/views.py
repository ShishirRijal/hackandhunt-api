from django.shortcuts import render
from rest_framework import viewsets

from apis.models.level import Level
from apis.serializers.level_serializer import LevelSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
