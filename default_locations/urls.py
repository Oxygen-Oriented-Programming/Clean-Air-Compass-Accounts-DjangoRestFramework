from django.urls import path
from .views import SetDefaultLocation, RUDDefaultLocation

urlpatterns = [
    path("create/", SetDefaultLocation.as_view()),
    path("<int:pk>/", RUDDefaultLocation.as_view()),
]