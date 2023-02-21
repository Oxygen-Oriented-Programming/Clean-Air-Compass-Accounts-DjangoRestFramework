from rest_framework import serializers
from .models import SmsAlert

class SmsAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsAlert
        fields = '__all__'
