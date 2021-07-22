from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .serializers import AdSerializer

from ad.models import Ad


class AdListCreateAPIView(ListCreateAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = AdSerializer

    def get_queryset(self):
        queryset = Ad.objects.all()
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
