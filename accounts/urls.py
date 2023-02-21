from django.urls import path
from .views import *

urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view()),
]
