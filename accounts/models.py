from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# This table is used for signup, login, and authentication process.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    opt_in_to_sms_alerts = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.DateTimeField(default=timezone.now)
    modified_by = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=100, default="normal")
    status = models.CharField(max_length=100, default="Active")
    auth_provider = models.CharField(max_length=50, blank=True, default="email")

    def __str__(self):
            return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'users'
