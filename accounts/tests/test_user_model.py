from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTests(TestCase):
    def test_user_created_with_defaults(self):
        u = User.objects.create_user(username="k1", password="StrongPass123!")
        self.assertEqual(u.preferred_currency, "BGN")
        self.assertEqual(u.timezone, "Europe/Sofia")

    def test_user_str_returns_username(self):
        u = User.objects.create_user(username="k2", password="StrongPass123!")
        self.assertEqual(str(u), "k2")