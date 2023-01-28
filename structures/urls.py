from django.urls import path
from .views import *

urlpatterns = [
    path('structures/create', StructureView.as_view(), name="create"),
    path('structures/list', get_structures_list, name="list"),
    path('structures/structure', get_structure, name="get"),
    path('structures/update', update_structure, name="update"),
    path('structures/delete', delete_structure, name="delete"),
    path('structures/search', search_structure, name="search"),
]
