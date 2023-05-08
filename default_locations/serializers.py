from rest_framework import serializers
from .models import DefaultLocation

class DefaultLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultLocation
        fields = '__all__'
