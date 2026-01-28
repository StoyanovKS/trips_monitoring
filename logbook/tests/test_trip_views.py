from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.tests.helpers import create_user
from garage.models import Car
from logbook.models import Trip

class TripViewsTests(TestCase):
    def setUp(self):
        self.owner = create_user("owner")
        self.other = create_user("other")
        self.car_owner = Car.objects.create(
            owner=self.owner, brand="VW", model="Golf", year=2018, fuel="diesel", gearbox="auto"
        )
        self.car_other = Car.objects.create(
            owner=self.other, brand="BMW", model="X3", year=2019, fuel="diesel", gearbox="auto"
        )
        self.trip_other = Trip.objects.create(
            car=self.car_other,
            created_by=self.other,
            start_odometer=100,
            end_odometer=200,
            start_date=timezone.localdate(),
            end_date=timezone.localdate(),
            from_city="A",
            to_city="B",
        )

    def test_trip_list_requires_login(self):
        resp = self.client.get(reverse("trip-list"))
        self.assertEqual(resp.status_code, 302)

    def test_trip_list_shows_only_trips_for_own_cars(self):
        self.client.login(username="owner", password="StrongPass123!")
        resp = self.client.get(reverse("trip-list"))
        self.assertEqual(resp.status_code, 200)
        # If your TripListView filters by car owner, other user's trip must not be visible
        trips = list(resp.context["object_list"])
        self.assertNotIn(self.trip_other, trips)

    def test_trip_detail_for_other_users_trip_is_forbidden_or_not_found(self):
        self.client.login(username="owner", password="StrongPass123!")
        resp = self.client.get(reverse("trip-detail", kwargs={"pk": self.trip_other.pk}))
        self.assertIn(resp.status_code, (403, 404))

    def test_trip_create_creates_trip_with_created_by(self):
        self.client.login(username="owner", password="StrongPass123!")
        resp = self.client.post(
            reverse("trip-create"),
            data={
                "car": self.car_owner.pk,
                "start_odometer": 10,
                "end_odometer": 30,
                "start_date": timezone.localdate(),
                "end_date": timezone.localdate(),
                "from_city": "Sofia",
                "to_city": "Plovdiv",
                "notes": "",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Trip.objects.filter(created_by=self.owner, car=self.car_owner).exists())