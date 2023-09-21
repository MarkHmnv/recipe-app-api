"""
Url mappings for the recipe API
"""
from recipe import views

from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.RecipeViewSet)

app_name = "recipes"

urlpatterns = [
    path("", include(router.urls)),
]
