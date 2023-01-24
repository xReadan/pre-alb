from django.urls import path
from .views import *

urlpatterns = [
    path('login', login),
    path('register', RegisterUserView.as_view(), name="register"),
    path('user', CurrentLoggedInUser.as_view({'get': 'retrieve'}), name='current_user'),
    path('update-user-settings', update_user_settings)
]