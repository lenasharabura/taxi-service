from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer(name="Ford", country="USA")

        self.assertEqual(str(manufacturer), "Ford USA")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="johndoe",
            password="123456user",
            first_name="John",
            last_name="Doe"
        )

        self.assertEqual(str(driver), "johndoe (John Doe)")

    def test_car_str(self):
        manufacturer = Manufacturer(name="Ford", country="USA")
        car = Car(model="Ford Mustang", manufacturer=manufacturer)

        self.assertEqual(str(car), "Ford Mustang")

    def test_create_driver_with_license_nummer(self):
        username = "johndoe"
        password = "123456user"
        first_name = "John"
        last_name = "Doe"
        license_number = "ASD12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, "ASD12345")
