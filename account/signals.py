from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from account.models import User
from account.utils import generate_key, generate_usernameX


@receiver(pre_save, sender=User)
def create_key(sender, instance, **kwargs):
    # GENERATING THE KEY FOR OTP.
    if not instance.key:
        instance.key = generate_key()


@receiver(pre_save, sender=User)
def generate_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = generate_usernameX()
