from django.urls import path
from .views import AdListCreateAPIView, AdsDetailDelete, add_to_favourite, remove_from_favourite

urlpatterns = [
    path('ads/', AdListCreateAPIView.as_view()),  # create, list
    path('ads/<int:id>/', AdsDetailDelete.as_view()),  # get detail, delete
    path('ads/<int:id>/add-to-favourite/', add_to_favourite),  # get like
    path('ads/<int:id>/remove-from-favourite/', remove_from_favourite)  # get unlike
]
