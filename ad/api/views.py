from django.shortcuts import get_object_or_404

from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

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
        favourites = self.request.query_params.get('favourites', None)
        user = self.request.query_params.get('user', None)
        if region:
            queryset = queryset.filter(region__icontains=region)
        if category:
            queryset = queryset.filter(category=category)
        if favourites:
            queryset = queryset.filter(liked=self.request.user)
        if user:
            queryset = queryset.filter(user=self.request.user)
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


class AdsDetailDelete(RetrieveDestroyAPIView, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = AdSerializer
    lookup_field = 'id'
    queryset = Ad.objects.all()

    def delete(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return self.destroy(self.request)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_to_favourite(request, id):
    ad = get_object_or_404(Ad, pk=id)
    if not ad.liked.filter(id=request.user.id).exists():
        ad.liked.add(request.user)
        return Response({'message': 'Added to favourites'}, status=status.HTTP_200_OK)
    return Response({'message': 'Already sdded to favourites'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def remove_from_favourite(request, id):
    ad = get_object_or_404(Ad, pk=id)
    if ad.liked.filter(id=request.user.id).exists():
        ad.liked.remove(request.user)
        return Response({'message': 'Removed from favourites'}, status=status.HTTP_200_OK)
    return Response({'message': 'Not in favourites favourites'}, status=status.HTTP_200_OK)
