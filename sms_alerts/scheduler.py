from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .sms_alerter import run_script

scheduler = BackgroundScheduler()

def start():
    scheduler.add_job(run_script, "interval", seconds=10)
    scheduler.start()
