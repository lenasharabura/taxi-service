from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
        get_user_model().objects.create(
            username="johnsmith",
            password="123456user",
            license_number="ASD11345",
        )
        get_user_model().objects.create(
            username="superman",
            password="123456user",
            license_number="AVD12345",
        )

        response = self.client.get(reverse("taxi:driver-list"))
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
