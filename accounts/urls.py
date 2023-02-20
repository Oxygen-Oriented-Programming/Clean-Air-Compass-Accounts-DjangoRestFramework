from django.urls import path
from .views import *

urlpatterns = [
    path("github/", GithubSocialAuthView.as_view()),
    path("google/", GoogleSocialAuthView.as_view()),
]
