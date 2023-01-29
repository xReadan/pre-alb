from django.urls import path
from .views import *

urlpatterns = [
    path('notifications/create-request', create_notification_request, name="create_request"),
    path('notifications/list', notification_list, name="notification_list"),
    path('notifications/check', check_user_notifications, name="check_user_notifications"),
]
