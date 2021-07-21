from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=100, blank=True)
    key = models.CharField(max_length=500, blank=True)

    fullname = models.CharField(max_length=100, default="")
    pic = models.ImageField(upload_to='users/pics', null=True, blank=True)

    def __str__(self):
        return self.username + " == "
