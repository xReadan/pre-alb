from django.urls import path
from .views import *

urlpatterns = [
    path('structures/create', StructureView.as_view(), name="create"),
    path('structures/list', get_structures_list, name="create")
]
