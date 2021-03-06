from django.db import models
from account.models import User
from category.models import Category

def default_location():
    return {
        'lon': '',
        'lat': ''
    }


class Image(models.Model):
    file = models.ImageField(upload_to='ads/pics')


class Ad(models.Model):
    TYPE_NORMAL = 'NORMAL'
    TYPE_COMPANY = 'COMPANY'
    TYPE_CAR = 'CAR'
    TYPE_CHOICES = (
        (TYPE_NORMAL, 'Normal'),
        (TYPE_COMPANY, 'Company'),
        (TYPE_CAR, 'Car'),
    )

    user = models.ForeignKey(User,related_name='posted_ads', on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_NORMAL, max_length=32)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    images = models.ManyToManyField(Image, blank=True)
    address = models.TextField(default='')  # full address text

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    liked = models.ManyToManyField(User, related_name='favourite_ads', blank=True)

    region = models.CharField(default='', max_length=100)

    location = models.JSONField(default=default_location)  # lon, lat
    extra = models.JSONField(null=True, blank=True)  # lon, lat
