from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from chat.api.serializers import ChatSerializer, MessageSerializer
from chat.models import Chat, Message

from django.shortcuts import get_object_or_404
from django.db.models import Q

from account.models import User


class ChatListAPI(ListAPIView, ListModelMixin):
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(Q(seller=self.request.user) | Q(buyer=self.request.user))


class MessageList(ListAPIView, ListModelMixin):
    serializer_class = MessageSerializer

    # todo add these code to chat_manager
    def get_queryset(self):
        queryset = []
        chat_id = self.request.query_params.get('ad', None)
        user_id = self.request.query_params.get('user', None)
        last_message_id = self.request.query_params.get('last_message_id', None)

        if chat_id is not None:
            chat = get_object_or_404(Chat, id=chat_id)
        else:
            user = get_object_or_404(User, id=user_id)
            if user == self.request.user:
                chat = Chat.objects.get_or_create_self_chat(self.request.user)
            else:
                chat = Chat.objects.get_or_create_personal_chat(self.request.user, user)

        if chat and chat.is_member(self.request.user):
            queryset = Message.objects.filter(Q(chat=chat) & Q(has_deleted=False)).order_by('-pk')

            if last_message_id:
                queryset = queryset.filter(Q(id__lt=last_message_id))

        return queryset
