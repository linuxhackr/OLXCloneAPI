from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from banner.models import Banner
from .serializers import BannerSerialixer


class BannerList(ListAPIView, ListModelMixin):
    serializer_class = BannerSerialixer
    queryset = Banner.objects.order_by('sequence')
