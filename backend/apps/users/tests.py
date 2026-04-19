from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class AuthApiTest(APITestCase):
    def test_user_can_register(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "student",
                "email": "student@phystech.edu",
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.data)
        self.assertTrue(response.data["user"]["is_phystech_student"])

    def test_user_can_login(self):
        get_user_model().objects.create_user(
            username="user",
            email="user@example.com",
            password="strongpass123",
        )

        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "user",
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_me_requires_auth(self):
        response = self.client.get("/api/auth/me/")

        self.assertEqual(response.status_code, 401)

    def test_me_returns_current_user(self):
        user = get_user_model().objects.create_user(
            username="student",
            email="student@phystech.edu",
            password="strongpass123",
        )
        self.client.force_authenticate(user)

        response = self.client.get("/api/auth/me/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "student")
        self.assertTrue(response.data["is_phystech_student"])
