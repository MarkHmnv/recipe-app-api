"""
Tests for the tags API
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer
from recipe.tests import utils


TAGS_URL = reverse("recipes:tag-list")


def detail_url(tag_id):
    return reverse("recipes:tag-detail", args=[tag_id])


class PublicTagsAPITests(TestCase):
    """Test unauthenticated API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.user = utils.create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_tags(self):
        """Test getting a list of tags"""
        utils.create_tag(user=self.user)
        utils.create_tag(user=self.user)

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user"""
        other_user = utils.create_user(email="other@example.com")
        utils.create_tag(user=other_user)
        tag = utils.create_tag(user=self.user)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)

    def test_update_tag(self):
        """Test updating a tag"""
        tag = utils.create_tag(self.user)

        payload = {"name": "New tag name"}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload["name"])

    def test_delete_tag(self):
        """Test delete a tag"""
        tag = utils.create_tag(self.user)

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())

    def test_filter_tags_assigned_to_recipe(self):
        """Test listing tags by those assigned to recipes"""
        tag1 = utils.create_tag(user=self.user, name="Tag 1")
        tag2 = utils.create_tag(user=self.user, name="Tag 2")
        recipe = utils.create_recipe(user=self.user, title="Recipe 1")
        recipe.tags.add(tag1)

        res = self.client.get(TAGS_URL, {"assigned_only": 1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique(self):
        """Test filtered tags returns unique items"""
        tag = utils.create_tag(user=self.user, name="Tag 1")
        utils.create_tag(user=self.user, name="Tag 2")
        recipe1 = utils.create_recipe(user=self.user, title="Recipe 1")
        recipe1.tags.add(tag)
        recipe2 = utils.create_recipe(user=self.user, title="Recipe 2")
        recipe2.tags.add(tag)

        res = self.client.get(TAGS_URL, {"assigned_only": 1})

        self.assertEqual(len(res.data), 1)
