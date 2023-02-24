from django.test import TestCase, override_settings
from sms_alerts.models import SmsAlert
from accounts.models import User
from django.core.exceptions import ImproperlyConfigured
from unittest.mock import patch
from django.conf import settings

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

    @patch('sms_alerts.models.TwilioClient')
    def test_send_message_on_creation(self, MockTwilioClient):
        message = 'Test Message'
        mock_client_instance = MockTwilioClient.return_value
        self.sms_alert.send_message_on_creation(message, twilio_client=mock_client_instance)
        mock_client_instance.send_message.assert_called_once_with(
            to=self.sms_alert.phone_number,
            from_=mock_client_instance.twilio_phone_number,
            body=message
        )
        
    @patch('sms_alerts.models.TwilioClient')
    @override_settings(TWILIO_AUTH_TOKEN=None)
    def test_send_message_on_creation_with_missing_twilio_credentials(self, MockTwilioClient):
        with self.assertRaises(ImproperlyConfigured):
            MockTwilioClient = None
            message = 'Test Message'
            mock_client_instance = MockTwilioClient
            self.sms_alert.send_message_on_creation(message, twilio_client=mock_client_instance)
            mock_client_instance.send_message.assert_called_once_with(
                to=self.sms_alert.phone_number,
                from_=mock_client_instance.twilio_phone_number,
                body=message
            )
