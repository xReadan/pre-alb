from django.urls import path
from .views import *

urlpatterns = [
    path('rooms/list', get_rooms_list, name="list"),
    path('rooms/create', create_room, name="create"),
    path('rooms/edit', edit_room, name="edit"),
    path('rooms/delete', delete_room, name="delete"),
    path('rooms/get', get_room_details, name="details"),
]
