from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_additional_arguments_is_valid(self):
        data = {
            "username": "johndoe",
            "password1": "123456user",
            "password2": "123456user",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@test.ua",
            "license_number": "ASD12345",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)
