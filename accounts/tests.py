from django.test import TestCase
from .models import User

class UserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass', email='testuser@example.com', first_name='Test', last_name='User')
    
    def test_string_representation(self):
        expected = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(str(self.user), expected)
