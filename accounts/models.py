from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    auth_provider = models.CharField(max_length=50)

    def __str__(self):
            return self.email
