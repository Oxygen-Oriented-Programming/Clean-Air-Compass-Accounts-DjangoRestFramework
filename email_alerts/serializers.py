from rest_framework import serializers
from .models import EmailAlert

class EmailAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAlert
        fields = '__all__'