from django.shortcuts import render, redirect
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import SmsAlert
from .serializers import SmsAlertSerializer
from rest_framework.permissions import IsAuthenticated
from .sms_alerter import query_fast_api, get_aqi_level
from textwrap import dedent
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

class SmsAlertList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SmsAlert.objects.all()
    serializer_class = SmsAlertSerializer

    def get_queryset(self):
        user = self.request.user
        return SmsAlert.objects.filter(user=user)

    def post(self, request, *arg, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        first_message = serializer.save(user=request.user)
        location = first_message.location
        latest_pm_25 = query_fast_api(location)
        aqi_level = get_aqi_level(latest_pm_25)
        message_body = dedent(f"""
        You will now receive alerts for {location}.\n
        Air quality in {location} is now {aqi_level[0]}.\n
        {aqi_level[1]}
        """)
        first_message.send_message_on_creation(message_body)
        return Response({"message": "SMS alert created successfully"}, status=HTTP_201_CREATED)


class SmsAlertDetail(RetrieveUpdateDestroyAPIView):
    queryset = SmsAlert.objects.all()
    serializer_class = SmsAlertSerializer
