from django.urls import path
from .auth_views import login, signup, update_account, get_user, send_otp, change_password, logout
urlpatterns = [
    path('auth/login/', login),
    path('auth/signup/', signup),
    path('auth/get-user/', get_user),
    path('auth/send-otp/', send_otp),
    path('auth/change-password/', change_password),
    path('auth/update/', update_account),
    path('auth/logout/', logout),
]
