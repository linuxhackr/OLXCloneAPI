import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from urllib import parse

from ad.models import Ad
from .api.serializers import MessageSerializer
from .models import Chat
from account.models import User

from django.db.models import Q


# wss://domain.com/ws/chat/?token=••••&user=••


class ChatConsumer(AsyncWebsocketConsumer):
    chat = None
    me = None

    async def connect(self):
        user_id = parse.parse_qs(self.scope['query_string'].decode("utf-8")).get('user', None)[0]
        self.me = self.scope['user']

        print(self.me, user_id)

        if not self.me.is_authenticated or user_id is None:
            print('NOT AUTHENTICATED ❌')
            await self.close()
            return

        print(1)
        # CHAT - get or create if not available.
        self.chat = await self.get_or_create_chat(self.me, user_id)
        print(2)

        print('CHAT is ',  self.chat)

        if self.chat is None:
            await self.close()
            return

        # GROUP NAME ~ CHAT NAME {add user to chat group}
        self.group_name = 'CHAT_ROOM_%s' % self.chat.id
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_ = json.loads(text_data)
        try:
            action = text_data_.get('action', None)
            if action == 'MESSAGE_SEND':
                message_text = text_data_.get('text', "")
                message = await self.create_message(message_text)
                if message:
                    print(3)
                    message = {
                        'action': action,
                        'message': MessageSerializer(message).data
                    }
                    print(4)
            else:
                return
            print('MESSAGE IS ',message)
            message and await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'broadcast_chat_message',
                    'message': message
                }
            )
        except KeyError:
            pass

    async def broadcast_chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_or_create_chat(self, me, user_id):
        user = User.objects.get(id=user_id)
        chats = Chat.objects.filter(
            Q(Q(seller=me) & Q(buyer=user)) | Q(Q(seller=user) & Q(buyer=me)))
        print(chats)
        if len(chats) == 1:
            print(chats.first())
            return chats.first()
        else:
            return Chat.objects.create(buyer=me, seller=user)

    @database_sync_to_async
    def create_message(self, message_text):
        print(self.chat, self.me)
        if message_text != "":
            if self.chat:
                message = self.chat.create_message(
                    user=self.me,
                    text=message_text)
                print(message, '...')
                return message
        return None


"""
SAMPLE_MESSAGE = {
    "action":"MESSAGE_SEND",
    "text":"some txt"
}
"""
