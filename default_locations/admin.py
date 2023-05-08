from django.contrib import admin
from .models import *

class DefaultLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_location')

admin.site.register(DefaultLocation, DefaultLocationAdmin)