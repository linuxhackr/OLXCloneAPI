from rest_framework.serializers import ModelSerializer

from account.api.serializers import UserSerializer
from ad.models import Ad, Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['file']


class AdSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'title', 'price', 'description', 'user', 'address', 'type', 'location', 'extra', 'images']
        read_only_fields = ['images']

    def create(self, validated_data):
        images = validated_data.pop('images', None)

        ad = Ad.objects.create(**validated_data)

        if images:
            for i in images:
                image = Image.objects.create(file=i)
                image.save()
                ad.images.add(image)
        ad.save()
        return ad
