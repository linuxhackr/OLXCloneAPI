from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from chat.api.serializers import ChatSerializer, MessageSerializer
from chat.models import Chat, Message

from django.shortcuts import get_object_or_404
from django.db.models import Q

from account.models import User


def get_or_create_chat(me, user_id):
    user = User.objects.get(id=user_id)
    chats = Chat.objects.filter(
        Q(Q(seller=me) & Q(buyer=user)) | Q(Q(seller=user) & Q(buyer=me)))
    if len(chats) == 1:
        return chats.first()
    else:
        return Chat.objects.create(buyer=me, seller=user)


class ChatListAPI(ListAPIView, ListModelMixin):
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(Q(seller=self.request.user) | Q(buyer=self.request.user))


class MessageList(ListAPIView, ListModelMixin):
    serializer_class = MessageSerializer

    # todo add these code to chat_manager
    def get_queryset(self):
        queryset = []
        user_id = self.request.query_params.get('user', None)
        last_message_id = self.request.query_params.get('last_message_id', None)

        if user_id is not None:
            chat = get_or_create_chat(self.request.user, user_id)
        else:
            chat = None

        if chat and chat.is_member(self.request.user):
            queryset = Message.objects.filter(Q(chat=chat)).order_by('-pk')

            if last_message_id:
                queryset = queryset.filter(Q(id__lt=last_message_id))

        return queryset
