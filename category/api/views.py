from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from .serializers import CategorySerializer
from category.models import Category


class CategoryList(ListAPIView, ListModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
