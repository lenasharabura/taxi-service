from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password12345",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="johndoe",
            password="123456user",
            first_name="John",
            last_name="Doe",
            license_number="ASD12345",
        )

    def test_driver_license_number_listed(self):
        """Test that the license number is listed on the admin driver page"""

        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        """Test that the license number is listed on the admin driver detail page"""

        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_create_additional_info_listed(self):
        """Test that the license number, first name and last name
         are listed on the admin driver create page"""

        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "License number")
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
