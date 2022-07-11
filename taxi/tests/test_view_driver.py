from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


class PublicDriverTests(TestCase):
    def test_login_required_list(self):
        """Test that only logged-in users can access the driver list page"""
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")

    def test_login_required_create(self):
        """Test that only logged-in users can access the driver create page"""

        response = self.client.get(reverse("taxi:driver-create"))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/create/")

    def test_login_required_update(self):
        """Test that only logged-in users can access the driver update page"""
        response = self.client.get(reverse("taxi:driver-update", args=[1]))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/1/update/")

    def test_login_required_delete(self):
        """Test that only logged-in users can access the driver delete page"""
        response = self.client.get(reverse("taxi:driver-delete", args=[1]))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/1/delete/")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="johndoe",
            password="123456user",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        self.driver = get_user_model().objects.create_user(
            username="johnsmith",
            password="123456user",
            license_number="ASD11345",
        )

        response = self.client.get(reverse("taxi:driver-list"))
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_car_create(self):
        form_data = {
            "username": "johnsmith",
            "password1": "123456user",
            "password2": "123456user",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@admin.ua",
            "license_number": "ASD11345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(new_driver.license_number, form_data["license_number"])
