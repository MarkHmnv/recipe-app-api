"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Tests without authentication"""
    def setUp(self):
        self.client = APIClient()
        self.user_payload = {
            "email": "test@example.com",
            "password": "password",
            "name": "Test Name"
        }

    def test_create_user_success(self):
        """Test create user successful"""
        res = self.client.post(CREATE_USER_URL, self.user_payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.user_payload["email"])
        self.assertTrue(user.check_password(self.user_payload["password"]))

    def test_user_with_email_exists_error(self):
        """Test an error is returned if user with email exists"""
        create_user(**self.user_payload)
        res = self.client.post(CREATE_USER_URL, self.user_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars"""
        self.user_payload["password"] = "psw"
        res = self.client.post(CREATE_USER_URL, self.user_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=self.user_payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_success(self):
        """Test generates token for valid credentials"""
        create_user(**self.user_payload)
        login_payload = {
            "email": self.user_payload["email"],
            "password": self.user_payload["password"]
        }
        res = self.client.post(TOKEN_URL, login_payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid"""
        create_user(**self.user_payload)
        login_payload = {
            "email": "invalid",
            "password": "invalid"
        }
        res = self.client.post(TOKEN_URL, login_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test returns error if password blank"""
        create_user(**self.user_payload)
        login_payload = {
            "email": self.user_payload["email"],
            "password": ""
        }
        res = self.client.post(TOKEN_URL, login_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for userss"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Tests with authentication"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="test@example.com",
            password="password",
            name="Test Name"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": self.user.name,
            "email": self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for me endpoint"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test update user profile successfully"""
        payload = {
            "name": "Updated name",
            "password": "newpassword"
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
