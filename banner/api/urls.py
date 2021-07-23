from django.urls import path
from .views import BannerList

urlpatterns = [
    path('banners/', BannerList.as_view())
]
