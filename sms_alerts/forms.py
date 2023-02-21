from django import forms
from .models import SmsAlert

class SmsAlertForm(forms.ModelForm):
    class Meta:
        model = SmsAlert
        fields = '__all__'
        widgets = {
            'username': forms.Select(attrs={'class': 'form-control'}),
        }
