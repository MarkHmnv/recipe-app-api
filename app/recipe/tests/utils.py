"""
Utils for tests
"""
from decimal import Decimal
from django.contrib.auth import get_user_model

from core.models import Ingredient, Tag, Recipe


def create_user(email="test@example.com", password="password", **extra_fields):
    return get_user_model().objects.create_user(email=email, password=password, **extra_fields)


def create_ingredient(user, name="Ingredient", **extra_fields):
    return Ingredient.objects.create(user=user, name=name, **extra_fields)


def create_tag(user, name="Tag", **extra_fields):
    return Tag.objects.create(user=user, name=name, **extra_fields)


def create_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        "title": "Sample recipe title",
        "time_minutes": 22,
        "price": Decimal("5.25"),
        "description": "Sample description",
        "link": "http://example.com/recipe.pdf",
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)
