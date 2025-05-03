from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

# from rest_framework.reverse import reverse as api_reverse


class TestRegistrationAPIView(APITestCase):
    def setUp(self):
        self.register_url = reverse(
            "authentication:user-registration"
        )  # Replace 'registration' with the actual name of your URL pattern

        self.valid_user_data = {
            "first_name": "testuser1",
            "last_name": "testuser2",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Password123",
        }
        self.invalid_user_data = {
            "username": "",
            "email": "invalidemail",
            "password": "123",
            "password2": "456",
        }

    def test_registration_with_valid_data(self):
        response = self.client.post(
            self.register_url, self.valid_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertIsInstance(response.data, dict)

    def test_registration_with_invalid_data(self):
        response = self.client.post(self.register_url, self.invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIsInstance(response.data, dict)
        self.assertIn("errors", response.data)
        self.assertEqual(
            response.data["errors"]["email"], ["Enter a valid email address."]
        )
        self.assertEqual(
            response.data["errors"]["username"], ["This field may not be blank."]
        )
        self.assertEqual(
            response.data["errors"]["password"][0],
            "Password must be at least 8 characters long.",
        )
        self.assertIsInstance(response.data["errors"], dict)
        self.assertEqual(
            response.data["errors"]["password"][1],
            "Password must have at least a number, and a least an uppercase and a lowercase letter.",
        )

    def test_registration_with_existing_email(self):
        # test if the email already exists
        self.client.post(self.register_url, self.valid_user_data, format="json")
        response = self.client.post(
            self.register_url, self.valid_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIsInstance(response.data, dict)
        self.assertIn("errors", response.data)
        self.assertIn("email", response.data["errors"])
        self.assertEqual(
            response.data["errors"]["email"], ["A user with that email already exists."]
        )

    def test_registration_with_existing_username(self):
        # test client with existing username
        self.client.post(self.register_url, self.valid_user_data, format="json")
        response = self.client.post(
            self.register_url, self.valid_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIsInstance(response.data, dict)
        self.assertIn("errors", response.data)
        self.assertIn("username", response.data["errors"])
        self.assertEqual(
            response.data["errors"]["username"],
            ["Username already exist."],
        )


class TestProfileApiView(APITestCase):
    def setUp(self):
        self.profile_url = reverse("authentication:users-profile")
        self.valid_user_data = {
            "first_name": "testuser1",
            "last_name": "testuser2",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Password123",
        }
