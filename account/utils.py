import pyotp
from django.utils.crypto import get_random_string
from account.models import User
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken


# used for forgot password
def get_short_lived_token(user):
    refresh_token = RefreshToken.for_user(user)
    return str(refresh_token)


# used for login
def get_token(user):
    refresh_token = RefreshToken.for_user(user)
    refresh_token.set_exp(lifetime=timedelta(days=7))  # EXTEND lifetime
    return str(refresh_token)


def is_username_unique(username):
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        return True
    return False


def generate_usernameX():
    """generate random username"""
    username = get_random_string(length=9, allowed_chars='1234567890')
    """convert into lower"""
    username = username.lower()
    if is_username_unique(username):
        return username
    generate_usernameX()


def generate_key():
    """ User otp key generator """
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    generate_key()


def is_unique(key):
    try:
        User.objects.get(key=key)
    except User.DoesNotExist:
        return True
    return False
