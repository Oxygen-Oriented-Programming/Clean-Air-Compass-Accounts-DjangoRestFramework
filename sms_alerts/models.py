import os
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from accounts.models import User


class SmsAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100,)
    air_quality_threshold = models.CharField(choices=[('Good','Good'), ('Moderate','Moderate'),('Unhealthy for Sensitive Groups','Unhealthy for Sensitive Groups'),('Unhealthy','Unhealthy'), ('Very Unhealthy','Very Unhealthy'),('Hazardous','Hazardous')], max_length=100)
    previous_air_quality_threshold_alert = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.location} - AQI {self.air_quality_threshold}'
