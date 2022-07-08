from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        self.car = Car.objects.create(model="Focus", manufacturer=self.manufacturer)

    def test_login_required_list(self):
        """Test that only logged-in users can access the car list page"""
        response = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/cars/")

    def test_login_required_create(self):
        """Test that only logged-in users can access the car create page"""

        response = self.client.get(reverse("taxi:car-create"))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/cars/create/")

    def test_login_required_update(self):
        """Test that only logged-in users can access the car update page"""
        response = self.client.get(reverse("taxi:car-update", args=[1]))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/cars/1/update/")

    def test_login_required_delete(self):
        """Test that only logged-in users can access the car delete page"""
        response = self.client.get(reverse("taxi:car-delete", args=[1]))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/cars/1/delete/")


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="johndoe",
            password="123456user",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(name="Ford", country="USA")

    def test_retrieve_car_list(self):
        Car.objects.create(model="Focus", manufacturer=self.manufacturer)
        Car.objects.create(model="Mustang", manufacturer=self.manufacturer)

        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

