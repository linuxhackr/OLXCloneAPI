import logging

import jwt, re
import traceback

from asgiref.sync import sync_to_async
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import LazySettings
from jwt import decode as jwt_decode

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from urllib import parse

from account.models import User

settings = LazySettings()


@sync_to_async
def validate_token(token):
    # Try to authenticate the user
    try:
        # This will automatically validate the token and raise an error if token is invalid
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        # Token is invalid
        print(e)
        return AnonymousUser()
    else:
        #  Then token is valid, decode it
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print(decoded_data)
        # Will return a dictionary like -
        # {
        #     "token_type": "access",
        #     "exp": 1568770772,
        #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
        #     "user_id": 6
        # }

        # Get the user using ID
        return User.objects.get(id=decoded_data["user_id"])


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        try:
            token = parse.parse_qs(scope['query_string'].decode("utf-8"))['token'][0] or ''
            if token:
                scope['user'] = await validate_token(token)
            else:
                scope['user'] = AnonymousUser()
            return await self.inner(scope, receive, send)
        except:
            scope['user'] = AnonymousUser()
            return await self.inner(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
