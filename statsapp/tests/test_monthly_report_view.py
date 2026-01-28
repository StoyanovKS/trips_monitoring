from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.tests.helpers import create_user
from garage.models import Car
from statsapp.models import MonthlyCarStat

class MonthlyReportViewTests(TestCase):
    def setUp(self):
        self.owner = create_user("owner")
        self.other = create_user("other")
        self.car_owner = Car.objects.create(
            owner=self.owner, brand="VW", model="Golf", year=2018, fuel="diesel", gearbox="auto"
        )
        today = timezone.localdate()
        MonthlyCarStat.objects.create(
            car=self.car_owner,
            year=today.year,
            month=today.month,
            trips_count=1,
            total_distance_km=100,
            refuels_count=1,
            total_fuel_liters="20.00",
            total_fuel_cost="60.00",
        )

    def test_monthly_report_requires_login(self):
        resp = self.client.get(reverse("monthly-report"))
        self.assertEqual(resp.status_code, 302)

    def test_monthly_report_renders_for_logged_user(self):
        self.client.login(username="owner", password="StrongPass123!")
        resp = self.client.get(reverse("monthly-report"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "statsapp/monthly_report.html")