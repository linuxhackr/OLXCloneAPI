from rest_framework.serializers import ModelSerializer
from account.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'fullname',
            'pic',
            'email',
        )
        read_only_fields = fields
