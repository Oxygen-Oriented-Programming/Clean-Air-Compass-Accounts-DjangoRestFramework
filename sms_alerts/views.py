from django.shortcuts import render, redirect
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import SmsAlert
from .serializers import SmsAlertSerializer
from rest_framework.permissions import IsAuthenticated

class SmsAlertList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SmsAlert.objects.all()
    serializer_class = SmsAlertSerializer

    def get_queryset(self):
        user = self.request.user
        return SmsAlert.objects.filter(user=user)


class SmsAlertDetail(RetrieveUpdateDestroyAPIView):
    queryset = SmsAlert.objects.all()
    serializer_class = SmsAlertSerializer
