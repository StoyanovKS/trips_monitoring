from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.tests.helpers import create_user
from garage.models import Car
from logbook.models import Trip

class TripModelTests(TestCase):
    def setUp(self):
        self.user = create_user("owner")
        self.car = Car.objects.create(
            owner=self.user,
            brand="VW",
            model="Golf",
            year=2018,
            fuel="diesel",
            gearbox="auto",
        )

    def test_distance_km_property(self):
        t = Trip(
            car=self.car,
            created_by=self.user,
            start_odometer=100,
            end_odometer=250,
            start_date=timezone.localdate(),
            end_date=timezone.localdate(),
            from_city="Sofia",
            to_city="Plovdiv",
        )
        self.assertEqual(t.distance_km, 150)

    def test_clean_raises_when_end_odometer_smaller(self):
        t = Trip(
            car=self.car,
            created_by=self.user,
            start_odometer=300,
            end_odometer=200,
            start_date=timezone.localdate(),
            end_date=timezone.localdate(),
            from_city="Sofia",
            to_city="Plovdiv",
        )
        with self.assertRaises(ValidationError):
            t.full_clean()

    def test_clean_raises_when_end_date_before_start_date(self):
        today = timezone.localdate()
        yesterday = today - timezone.timedelta(days=1)
        t = Trip(
            car=self.car,
            created_by=self.user,
            start_odometer=100,
            end_odometer=200,
            start_date=today,
            end_date=yesterday,
            from_city="Sofia",
            to_city="Plovdiv",
        )
        with self.assertRaises(ValidationError):
            t.full_clean()