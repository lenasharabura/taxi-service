from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class PublicManufacturerTests(TestCase):
    def test_login_required_list(self):
        """Test that only logged-in users can access the manufacturers list page"""
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")

    def test_login_required_create(self):
        """Test that only logged-in users can access the manufacturer create page"""

        response = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/create/")

    def test_login_required_update(self):
        """Test that only logged-in users can access the manufacturer update page"""
        Manufacturer.objects.create(name="Ford", country="USA")
        response = self.client.get(reverse("taxi:manufacturer-update", args=[1]))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/1/")

    def test_login_required_delete(self):
        """Test that only logged-in users can access the manufacturer delete page"""
        Manufacturer.objects.create(name="Ford", country="USA")
        response = self.client.get(reverse("taxi:manufacturer-delete", args=[1]))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/1/delete/")


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="johndoe",
            password="123456user",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Toyota", country="Japan")

        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
