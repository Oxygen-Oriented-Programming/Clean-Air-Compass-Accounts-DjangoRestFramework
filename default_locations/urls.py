from django.urls import path
from .views import SetDefaultLocation, RUDDefaultLocation

urlpatterns = [
    path("create/", SetDefaultLocation.as_view()),
    path("<str:pk>/", RUDDefaultLocation.as_view()),
]