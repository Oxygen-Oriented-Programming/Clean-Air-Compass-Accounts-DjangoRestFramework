from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ("email","created_date")

admin.site.register(User, CustomUserAdmin)