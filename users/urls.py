from django.urls import path
from .views import *

urlpatterns = [
    path('users/login', login),
    path('users/logout', user_logout),
    path('users/register', RegisterUserView.as_view(), name="register"),
    path('users/user', CurrentLoggedInUser.as_view({'get': 'retrieve'}), name='current_user'),
    path('users/update-user-settings', update_user_settings)
]