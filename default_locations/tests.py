from .models import DefaultLocation
from accounts.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase

class SmsAlertTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser", password="testpass", email='testuser@example.com'
        )
        testuser1.save()

        test_location = DefaultLocation.objects.create(
            user=testuser1,
            default_location='seattle'
        )
        test_location.save()

    def setUp(self):
        self.client.login(username='testuser',password='pass')

    def test_location_model(self):
        actual_user = User.objects.get(email='testuser@example.com')
        item = DefaultLocation.objects.get(user=actual_user)
        actual_location = str(item.default_location)
        self.assertEqual(actual_user.username, "testuser")
        self.assertEqual(actual_location, "seattle")
