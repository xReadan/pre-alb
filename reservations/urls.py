from django.urls import path
from .views import *

urlpatterns = [
    path('reservations/create', create_reservation, name="create"),
    path('reservations/list', get_user_reservation, name="get_user"),
    path('reservations/delete', delete_reservation, name="delete_reservation"),
]
