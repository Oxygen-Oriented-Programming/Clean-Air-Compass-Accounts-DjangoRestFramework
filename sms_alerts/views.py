from django.shortcuts import render, redirect
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import SmsAlert
from .serializers import SmsAlertSerializer
from .forms import SmsAlertForm


class SmsAlertList(ListCreateAPIView):
    queryset = SmsAlert.objects.all()
    serializer_class = SmsAlertSerializer


class SmsAlertDetail(RetrieveUpdateDestroyAPIView):
    queryset = SmsAlert.objects.all()
    serializer_class = SmsAlertSerializer


def create_sms_alert(request):
    if request.method == 'POST':
        form = SmsAlertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = SmsAlertForm()
    return render(request, '', {'form': form})
