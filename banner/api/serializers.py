from rest_framework.serializers import ModelSerializer
from banner.models import Banner


class BannerSerialixer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image', 'sequence']
