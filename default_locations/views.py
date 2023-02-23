from django.shortcuts import render
from django.shortcuts import render, redirect
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import DefaultLocation
from .serializers import DefaultLocationSerializer
from rest_framework.permissions import IsAuthenticated


class SetDefaultLocation(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = DefaultLocation.objects.all()
    serializer_class = DefaultLocationSerializer


class RUDDefaultLocation(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = DefaultLocation.objects.all()
    serializer_class = DefaultLocationSerializer
