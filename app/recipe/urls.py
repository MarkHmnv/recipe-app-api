"""
Url mappings for the recipe API
"""
from recipe import views

from django.urls import path, include

from rest_framework.routers import DefaultRouter

app_name = "recipes"

router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)
router.register("tags", views.TagViewSet)
router.register("ingredients", views.IngredientViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
