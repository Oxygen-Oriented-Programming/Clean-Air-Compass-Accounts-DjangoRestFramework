import os
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from accounts.models import User


class SmsAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, default=models.DefaultLocation.default_location)
    air_quality_threshold = models.CharField(choices=['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous'], max_length=50)
    previous_air_quality_threshold_alert = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.location} - AQI {self.air_quality_threshold}'

class DefaultLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    default_location = models.CharField(max_length=100, default='Chicago')
