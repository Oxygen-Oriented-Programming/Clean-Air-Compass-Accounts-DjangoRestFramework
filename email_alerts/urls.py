from django.urls import path
from . import views

urlpatterns = [
    path('cron/', views.cron.as_view()),
    path("create/", views.EmailAlertList.as_view()),
    path("<int:pk>/", views.EmailAlertDetail.as_view()),
]
