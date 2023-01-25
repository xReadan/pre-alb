from django.shortcuts import render
from .models import Structures
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import StructureSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

class StructureView(CreateAPIView):
    queryset = Structures.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StructureSerializer

@api_view(['POST'])
def get_structures_list(request):
    user_id = request.data.get('id')
    structures = list(Structures.objects.filter(owner_id = user_id).values())
    return JsonResponse(structures, safe=False)