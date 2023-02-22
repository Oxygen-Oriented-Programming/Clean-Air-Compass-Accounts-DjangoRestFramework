from django.apps import AppConfig
from django.conf import settings

class SmsAlertsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms_alerts'

    def ready(self):
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()
