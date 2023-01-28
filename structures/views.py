from django.shortcuts import render
from .models import Structures
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import StructureSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import exceptions

class StructureView(CreateAPIView):
    queryset = Structures.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StructureSerializer

@api_view(['POST'])
def get_structures_list(request):
    user_id = request.data.get('id')
    structures = list(Structures.objects.filter(owner_id = user_id).values())
    return JsonResponse(structures, safe=False)

@api_view(['POST'])
def get_structure(request):
    user_id = request.data.get('owner_id')
    structure_id = request.data.get('structure_id')
    # Get structure
    structure = Structures.objects.filter(id = structure_id).values().first()
    if structure['owner_id'] is not user_id:
        raise exceptions.PermissionDenied("Somethings went wrong")
    return JsonResponse(structure, safe=False)

@api_view(['POST'])
def update_structure(request):
    user_id = request.data.get('owner_id')
    structure_id = request.data.get('id')
    # Get structure
    structure = Structures.objects.filter(id = structure_id).first()
    if not structure or structure.owner_id is not user_id:
        raise exceptions.PermissionDenied("Somethings went wrong")
    # Check City
    city = request.data.get('city')
    if city:
        structure.city = city
    # Check address
    address = request.data.get('address')
    if city:
        structure.address = address
    # Check address
    rooms = request.data.get('rooms')
    if city:
        structure.rooms = rooms
    # Check address
    image = request.data.get('image')
    if city:
        structure.image = image
    # Save
    structure.save()
    return Response(f"{structure.name} updated")

@api_view(['POST'])
def delete_structure(request):
    user_id = request.data.get('owner_id')
    structure_id = request.data.get('structure_id')
    # Get structure
    structure = Structures.objects.filter(id = structure_id).first()
    if not structure or structure.owner_id is not user_id:
        raise exceptions.PermissionDenied("Somethings went wrong")
    # Delete
    structure.delete()
    return Response("Structure deleted!")