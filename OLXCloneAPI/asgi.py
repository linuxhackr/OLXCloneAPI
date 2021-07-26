import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.security.websocket import AllowedHostsOriginValidator

from chat.consumers import ChatConsumer
from OLXCloneAPI.token_auth import TokenAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OLXCloneAPI.settings')
django.setup()

# ASGI run alongside WSGI https://medium.com/@Ritiktaneja/configuring-asgi-django-application-using-daphne-and-nginx-server-59a90456fe17

websocket_urlpatterns = [
    url('ws/chat/', ChatConsumer.as_asgi()),

]

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    )
})
