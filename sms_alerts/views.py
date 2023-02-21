from django.shortcuts import render, redirect
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import SmsAlert
from .serializers import SmsAlertSerializer


class SmsAlertList(ListCreateAPIView):
    queryset = SmsAlert.objects.all()
    serializer_class = SmsAlertSerializer


class SmsAlertDetail(RetrieveUpdateDestroyAPIView):
    queryset = SmsAlert.objects.all()
    serializer_class = SmsAlertSerializer
