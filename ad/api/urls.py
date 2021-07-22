from django.urls import path
from .views import AdListCreateAPIView

urlpatterns = [
    path('ads/', AdListCreateAPIView.as_view()),  # create, list
    # path('ads/<int:id>/')  # get detail, delete
]
