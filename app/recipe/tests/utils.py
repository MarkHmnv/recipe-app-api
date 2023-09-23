"""
Utils for tests
"""
from django.contrib.auth import get_user_model


def create_user(email="test@example.com", password="password"):
    return get_user_model().objects.create_user(email=email, password=password)
