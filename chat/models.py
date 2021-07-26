from django.db import models
from ad.models import Ad
from account.models import User


class Chat(models.Model):
    seller = models.ForeignKey(User, related_name='seller_chats', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='buyer_chats', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('seller', 'buyer')

    def create_message(self, user, text):
        if not self.is_member(user):
            return None
        return self.messages.create(user=user, text=text)

    def get_last_message(self):
        return self.messages.last()

    def is_member(self, user):
        return self.seller == user or self.buyer == user


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)

    text = models.TextField(max_length=512, default="")
