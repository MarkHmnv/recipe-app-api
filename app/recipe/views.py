"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class BaseViewSet(viewsets.ModelViewSet):
    """Base view set"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class BaseRecipeAttrViewSet(BaseViewSet):
    """Base view set for recipe attributes"""
    def get_queryset(self):
        """Retrieve attribute for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class RecipeViewSet(BaseViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == "list":
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """View for manage tag APIs"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """View for manage ingredient APIs"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

