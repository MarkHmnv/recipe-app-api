"""
Tests for ingredients API
"""
from decimal import Decimal

from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient, Recipe

from recipe.serializers import IngredientSerializer
from recipe.tests import utils

INGREDIENTS_URL = reverse("recipes:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    """Test unauthenticated API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingredients"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.user = utils.create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients"""
        utils.create_ingredient(user=self.user)
        utils.create_ingredient(user=self.user)

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user"""
        other_user = utils.create_user(email="other@example.com", password="password")
        utils.create_ingredient(user=other_user)
        ingredient = utils.create_ingredient(user=self.user)

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)
        self.assertEqual(res.data[0]["id"], ingredient.id)

    def test_filter_ingredients_assigned_to_recipe(self):
        """Test listing ingredients by those assigned to recipes"""
        in1 = utils.create_ingredient(user=self.user, name="Ingredient 1")
        in2 = utils.create_ingredient(user=self.user, name="Ingredient 2")
        recipe = utils.create_recipe(user=self.user, title="Recipe 1")
        recipe.ingredients.add(in1)

        res = self.client.get(INGREDIENTS_URL, {"assigned_only": 1})

        s1 = IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_ingredients_unique(self):
        """Test filtered ingredients returns unique items"""
        ing = utils.create_ingredient(user=self.user, name="Ingredient 1")
        utils.create_ingredient(user=self.user, name="Ingredient 2")
        recipe1 = utils.create_recipe(user=self.user, title="Recipe 1")
        recipe1.ingredients.add(ing)
        recipe2 = utils.create_recipe(user=self.user, title="Recipe 2")
        recipe2.ingredients.add(ing)

        res = self.client.get(INGREDIENTS_URL, {"assigned_only": 1})

        self.assertEqual(len(res.data), 1)


