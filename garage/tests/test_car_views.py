from django.test import TestCase
from django.urls import reverse

from core.tests.helpers import create_user
from garage.models import Car


class CarViewsTests(TestCase):
    def setUp(self):
        self.owner = create_user("owner")
        self.other = create_user("other")

        fuel_field = Car._meta.get_field("fuel")
        gearbox_field = Car._meta.get_field("gearbox")

        self.fuel_value = fuel_field.choices[0][0] if fuel_field.choices else "diesel"
        self.gearbox_value = gearbox_field.choices[0][0] if gearbox_field.choices else "manual"

        self.car1 = Car.objects.create(
            owner=self.owner,
            brand="VW",
            model="Golf",
            year=2018,
            fuel=self.fuel_value,
            gearbox=self.gearbox_value,
        )
        self.car2 = Car.objects.create(
            owner=self.other,
            brand="BMW",
            model="X3",
            year=2019,
            fuel=self.fuel_value,
            gearbox=self.gearbox_value,
        )

    def test_car_list_requires_login(self):
        resp = self.client.get(reverse("car-list"))
        self.assertEqual(resp.status_code, 302)

    def test_car_list_shows_only_own_cars(self):
        self.client.login(username="owner", password="StrongPass123!")
        resp = self.client.get(reverse("car-list"))
        self.assertEqual(resp.status_code, 200)

        cars = list(resp.context["object_list"])
        self.assertIn(self.car1, cars)
        self.assertNotIn(self.car2, cars)

    def test_car_detail_for_other_users_car_is_forbidden_or_not_found(self):
        self.client.login(username="owner", password="StrongPass123!")
        resp = self.client.get(reverse("car-detail", kwargs={"pk": self.car2.pk}))
        self.assertIn(resp.status_code, (403, 404))

    def test_car_create_creates_car_for_logged_in_user(self):
        self.client.login(username="owner", password="StrongPass123!")

        resp = self.client.post(
            reverse("car-create"),
            data={
                "brand": "Audi",
                "model": "A4",
                "year": 2017,
                "fuel": self.fuel_value,
                "gearbox": self.gearbox_value,
            },
        )

        if resp.status_code == 200:
            print(resp.context["form"].errors)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Car.objects.filter(owner=self.owner, brand="Audi", model="A4").exists())
