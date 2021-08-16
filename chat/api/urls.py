from django.urls import path
from .views import ChatListAPI, MessageList
urlpatterns = [
    path('chats/',ChatListAPI.as_view()),
    path('messages/',MessageList.as_view()),
]