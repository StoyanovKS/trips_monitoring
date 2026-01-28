from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthViewsTests(TestCase):
    def test_login_page_renders(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "accounts/login.html")

    def test_register_creates_user_and_redirects(self):
        resp = self.client.post(
            reverse("register"),
            data={
                "username": "newuser",
                "email": "newuser@test.com",
                "preferred_currency": "BGN",
                "timezone": "Europe/Sofia",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        if resp.status_code == 200:
            print(resp.context["form"].errors)

        self.assertEqual(resp.status_code, 302)

    def test_logout_redirects(self):
        user = User.objects.create_user(username="u1", password="StrongPass123!")
        self.client.login(username="u1", password="StrongPass123!")
        resp = self.client.post(reverse("logout"))  
        self.assertEqual(resp.status_code, 302)