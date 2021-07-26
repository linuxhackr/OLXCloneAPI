from account.api.serializers import UserSerializer
from ad.api.serializers import AdSerializer
from chat.models import Chat, Message
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from OLXCloneAPI.utilities import get_time


class MessageSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    time = SerializerMethodField(required=False, read_only=True)

    class Meta(object):
        model = Message
        fields = ('id', 'text', 'chat', 'time', 'user',)

    def get_time(self, instance):
        return get_time(instance.date_created)


class ChatSerializer(ModelSerializer):
    seller = UserSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)
    ad = AdSerializer(read_only=True)
    last_message = SerializerMethodField(required=False, read_only=True)

    class Meta(object):
        model = Chat
        fields = ('id', 'ad', 'seller', 'buyer', 'last_message')

    def get_last_message(self, instance):
        last_message = instance.get_last_message()
        return MessageSerializer(last_message, context=self.context).data
