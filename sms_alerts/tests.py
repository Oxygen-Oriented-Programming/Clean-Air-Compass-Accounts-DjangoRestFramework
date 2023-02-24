from django.test import TestCase
from sms_alerts.models import SmsAlert
from accounts.models import User


class SmsAlertTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass', email='testuser@example.com')
        self.sms_alert = SmsAlert.objects.create(
            user=self.user,
            phone_number='8302795914',
            location='Seattle',
            air_quality_threshold='Good'
        )

    def test_sms_alert_created(self):
        self.assertEqual(self.sms_alert.user, self.user)
        self.assertEqual(self.sms_alert.phone_number, '8302795914')
        self.assertEqual(self.sms_alert.location, 'Seattle')
        self.assertEqual(self.sms_alert.air_quality_threshold, 'Good')
        self.assertEqual(self.sms_alert.previous_air_quality_threshold_alert, '')

    def test_sms_alert_string_representation(self):
        expected_string = f'{self.user.username} - Seattle - AQI Good'
        self.assertEqual(str(self.sms_alert), expected_string)
