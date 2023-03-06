from django.db import models
from django.core.exceptions import ImproperlyConfigured
from accounts.models import User
from django.conf import settings
from twilio.rest import Client

class TwilioClient:
    def __init__(self, account_sid=settings.TWILIO_ACCOUNT_SID, auth_token=settings.TWILIO_AUTH_TOKEN, twilio_phone_number=settings.TWILIO_PHONE_NUMBER):
        self.client = Client(account_sid, auth_token)
        self.twilio_phone_number = twilio_phone_number
    
    def send_message(self, to, from_, body):
        self.client.messages.create(
            to=to,
            from_=from_,
            body=body,
        )

class SmsAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerts")
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100,)
    air_quality_threshold = models.CharField(choices=[('Good','Good'), ('Moderate','Moderate'),('Unhealthy for Sensitive Groups','Unhealthy for Sensitive Groups'),('Unhealthy','Unhealthy'), ('Very Unhealthy','Very Unhealthy'),('Hazardous','Hazardous')], max_length=100)
    previous_air_quality_threshold_alert = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.location} - AQI {self.air_quality_threshold}'

    def send_message_on_creation(self, message, twilio_client=None):
        if not twilio_client:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            twilio_phone_number = settings.TWILIO_PHONE_NUMBER

            if not account_sid or not auth_token or not twilio_phone_number:
                raise ImproperlyConfigured('Twilio credentials not set')

            twilio_client = TwilioClient(account_sid, auth_token, twilio_phone_number)
        
        twilio_client.send_message(
            to=self.phone_number,
            from_=twilio_client.twilio_phone_number,
            body=message
        )
