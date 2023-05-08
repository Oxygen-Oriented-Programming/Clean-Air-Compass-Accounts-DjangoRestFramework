from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from smtplib import SMTPException
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.status import HTTP_201_CREATED
from textwrap import dedent
from .models import EmailAlert
from .serializers import EmailAlertSerializer
from django.conf import settings
fast_api_base_url = settings.FAST_API_BASE_URL
alerts = EmailAlert.objects.all()


def query_fast_api(location):
    url = fast_api_base_url + "average_pollution/" + location.lower()
    response = requests.get(url)
    
    return response.json()

def get_aqi_level(pm_25):
    levels = {
        (0, 6.0): ("Good", "Low", "Air quality is deemed acceptable and presents minimal hazard."),
        (6.0, 12.0): ("Good", "High", "Individuals who are sensitive should refrain from outdoor activities to prevent respiratory symptoms from occurring."),
        (12.0, 23.0): ("Moderate", "Low", "Sensitive individuals, as well as the general public, face the possibility of encountering respiratory issues and irritation."),
        (23.0, 33.0): ("Moderate", "High", "The general public is more likely to experience negative impacts and further strain on their heart and lungs."),
        (33.0, 41.0): ("Unhealthy for Sensitive Groups", "Low", "The impact on the general public will be significant, and vulnerable individuals should limit their outdoor activities."),
        (41.0, 55.0): ("Unhealthy for Sensitive Groups", "High", "The general public is highly susceptible to experiencing severe irritations and negative health impacts and is advised to refrain from engaging in outdoor activities."),
        (55.0, 155.0): ("Unhealthy","", "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."),
        (155.0, 250.0): ("Very Unhealthy", "","Health warnings of emergency conditions. The entire population is more likely to be affected."),
        (250.5, float('inf')): ("Hazardous","", "Health alert: everyone may experience more serious health effects. Avoid outdoor activities.")
    }

    for (lower, upper), (label,label2, message) in levels.items():
        if lower < pm_25 <= upper:
            return (label, message, pm_25, label2)
        
class cron(APIView):

    def get(self, request):
        for alert in alerts:
            location = alert.location
            aqi = query_fast_api(location)
            aqi_level = get_aqi_level(aqi)
            message = dedent(f"""
            Air quality in {alert.location.capitalize()} is now {aqi_level[0]} - {aqi_level[3]}. The hourly PM2.5 average is {round(aqi_level[2],1)}.\n
            {aqi_level[1]}""")
            if aqi_level[0] != alert.previous_air_quality:
                alert.previous_air_quality = aqi_level[0]
                alert.save()

            if aqi_level[0] == alert.air_quality and aqi_level[0] != alert.previous_air_quality:
                print("sending email")
                send_mail(
                    'Air Quality Alert',
                    message,
                    settings.EMAIL_HOST_USER,
                    [alert.email_to_alert],
                    fail_silently=False,
                )
        return Response(status=200)

class EmailAlertList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = EmailAlert.objects.all()
    serializer_class = EmailAlertSerializer

    def get_queryset(self):
        user = self.request.user
        return EmailAlert.objects.filter(user=user)


    def post(self, request, *arg, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        first_message = serializer.save(user=request.user)
        location = first_message.location
        latest_pm_25 = query_fast_api(location)
        aqi_level = get_aqi_level(latest_pm_25)
        first_message.previous_air_quality = aqi_level[0]
        first_message.save()
        message_body = dedent(f"""
        You will now receive alerts for {location.capitalize()}.\n
        Air quality in {location.capitalize()} is now {aqi_level[0]} - {aqi_level[3]}. The hourly PM2.5 average is {round(aqi_level[2],1)}. \n
        {aqi_level[1]}""")
        first_message.send_message_on_creation(message_body)
        return Response({"message": "Email alert created successfully"}, status=HTTP_201_CREATED)


class EmailAlertDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = EmailAlert.objects.all()
    serializer_class = EmailAlertSerializer