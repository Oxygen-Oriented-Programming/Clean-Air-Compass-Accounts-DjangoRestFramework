import os
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from accounts.models import User
from twilio.rest import Client

NOT_CONFIGURED_MESSAGE = (
    "Required environment variables "
    "TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing."
)

class SmsAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opt_in = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    air_quality_threshold = models.IntegerField()
    air_quality_direction = models.CharField(choices=[('below', 'Below'), ('above', 'Above')], max_length=5)

    def __str__(self):
        return f'{self.user.username} - {self.location} - AQI {self.air_quality_direction} {self.air_quality_threshold}'

    def send_alert(self):
        
        # Get the user's phone number
        phone_number = self.user.phone_number
        
        # Construct the message
        message = f"Air quality in {self.location} is now {self.air_quality_direction} {self.air_quality_threshold}."
        
        # Send the message using Twilio or another SMS service
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_= os.environ.get("TWILIO_PHONE_NUMBER", ""),
            to=phone_number
        )
        return message.sid
