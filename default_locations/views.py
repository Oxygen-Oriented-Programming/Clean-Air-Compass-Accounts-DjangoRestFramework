from django.shortcuts import render
from django.shortcuts import render, redirect
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import DefaultLocation
from .serializers import DefaultLocationSerializer


class SetDefaultLocation(CreateAPIView):
    queryset = DefaultLocation.objects.all()
    serializer_class = DefaultLocationSerializer


class RUDDefaultLocation(RetrieveUpdateDestroyAPIView):
    queryset = DefaultLocation.objects.all()
    serializer_class = DefaultLocationSerializer
