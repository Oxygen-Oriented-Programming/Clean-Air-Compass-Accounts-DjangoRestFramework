from django.contrib import admin
from .models import *

class SmsAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')

admin.site.register(SmsAlert, SmsAlertAdmin)