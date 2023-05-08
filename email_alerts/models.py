from django.db import models
from accounts.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError
from smtplib import SMTPException
from rest_framework.response import Response
from rest_framework import status

class EmailAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerts")
    email_to_alert = models.CharField(max_length=500,)
    location = models.CharField(max_length=100,)
    air_quality = models.CharField(max_length=100)
    previous_air_quality = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.location} - AQI {self.air_quality} - Previous Value is {self.previous_air_quality}'

    def send_message_on_creation(self, message):
        try:
            send_mail(
                    'Welcome to Clean Air Compass Alerts',
                    message,
                    settings.EMAIL_HOST_USER,
                    [self.email_to_alert],
                    fail_silently=False,
                )
        except (BadHeaderError, SMTPException) as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)