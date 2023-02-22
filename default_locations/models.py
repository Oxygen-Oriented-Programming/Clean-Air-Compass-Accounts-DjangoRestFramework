from django.db import models
from accounts.models import User


class DefaultLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_location = models.CharField(max_length=100, default='Chicago', primary_key=True)
