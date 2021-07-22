from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .serializers import AdSerializer

from ad.models import Ad


class AdListCreateAPIView(ListCreateAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = AdSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'price']

    def get_queryset(self):
        queryset = Ad.objects.all()
        region = self.request.query_params.get('region', None)
        category = self.request.query_params.get('category', None)
        if region:
            queryset = queryset.filter(region__icontains=region)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def perform_create(self, serializer):
        try:
            images = self.request.data.pop('images', None)
        except AttributeError:
            images = None

        serializer.save(
            user=self.request.user,
            images=images
        )
