from django.urls import path
from .views import SmsAlertList, SmsAlertDetail

urlpatterns = [
    path("create/", SmsAlertList.as_view()),
    path("<int:pk>/", SmsAlertDetail.as_view()),
]

from apscheduler.schedulers.background import BackgroundScheduler
from .sms_alerter import run_script

scheduler = BackgroundScheduler()
scheduler.add_job(run_script, trigger="cron", hour=1, max_instances=1)
scheduler.start()
