from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils import timezone

from core.tests.helpers import create_user
from garage.models import Car
from logbook.models import Trip, Refuel

class ApiEndpointsTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.owner = create_user("owner")
        self.other = create_user("other")

        self.car_owner = Car.objects.create(
            owner=self.owner, brand="VW", model="Golf", year=2018, fuel="diesel", gearbox="auto"
        )
        self.car_other = Car.objects.create(
            owner=self.other, brand="BMW", model="X3", year=2019, fuel="diesel", gearbox="auto"
        )

        Trip.objects.create(
            car=self.car_owner,
            created_by=self.owner,
            start_odometer=100,
            end_odometer=180,
            start_date=timezone.localdate(),
            end_date=timezone.localdate(),
            from_city="Sofia",
            to_city="Plovdiv",
        )
        Refuel.objects.create(
            car=self.car_owner,
            created_by=self.owner,
            date=timezone.localdate(),
            odometer=180,
            liters="20.00",
            total_cost="60.00",
            fuel_type="diesel",
            station="OMV",
        )

    def test_owner_can_access_car_stats(self):
        self.client_api.force_authenticate(user=self.owner)
        url = reverse("api-car-stats", kwargs={"car_id": self.car_owner.pk})
        resp = self.client_api.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("total_distance_km", resp.data)
        self.assertIn("refuels_count", resp.data)

    def test_non_owner_cannot_access_car_stats(self):
        self.client_api.force_authenticate(user=self.owner)
        url = reverse("api-car-stats", kwargs={"car_id": self.car_other.pk})
        resp = self.client_api.get(url)
        self.assertIn(resp.status_code, (403, 404))

    def test_owner_can_access_car_trips(self):
        self.client_api.force_authenticate(user=self.owner)
        url = reverse("api-car-trips", kwargs={"car_id": self.car_owner.pk})
        resp = self.client_api.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.data, list)
        self.assertGreaterEqual(len(resp.data), 1)

    def test_non_owner_cannot_access_car_trips(self):
        self.client_api.force_authenticate(user=self.owner)
        url = reverse("api-car-trips", kwargs={"car_id": self.car_other.pk})
        resp = self.client_api.get(url)
        self.assertIn(resp.status_code, (403, 404))
