from django.shortcuts import render
from structures.models import Structures
from .models import StructureRooms
from .serializers import StructureRoomsSerializer
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(['POST'])
def get_rooms_list(request):
    structure_id = request.data.get('structure_id')
    # Get structure
    structure = Structures.objects.filter(id = structure_id).first()
    # Get rooms
    rooms = list(StructureRooms.objects.filter(structure_id = structure.id).values())
    return JsonResponse(rooms, safe=False)

@api_view(['POST'])
def create_room(request):
    user_id = request.data.get('owner_id')
    room_data = request.data.get('room')
    structure = Structures.objects.filter(id = room_data['structure_id']).first()
    if not structure or structure.owner_id is not user_id:
        raise exceptions.PermissionDenied("You cant perform this actions")
    # Create data structure
    data = {'name': room_data['name'], 
        'description': room_data['description'], 
        'price': room_data['price'], 
        'image': room_data['image'], 
        'structure': structure.id}
    # Serialize data
    serializer = StructureRoomsSerializer(data=data)
    # Check data
    if serializer.is_valid():
        serializer.save()
        return Response("Room created")
    else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def edit_room(request):
    user_id = request.data.get('owner_id')
    room_data = request.data.get('room')
    structure = Structures.objects.filter(id = room_data['structure_id']).first()
    if not structure or structure.owner_id is not user_id:
        raise exceptions.PermissionDenied("You cant perform this actions")
            # Create data structure
    data = {'id': room_data['id'],
        'name': room_data['name'], 
        'description': room_data['description'], 
        'price': room_data['price'], 
        'image': room_data['image'], 
        'structure': structure.id}
    # Serialize data
    serializer = StructureRoomsSerializer(data=data)
    # Check data
    if serializer.is_valid():
        # Get room
        room = StructureRooms.objects.filter(id=room_data['id']).first()
        # Update info
        room.name = room_data['name']
        room.description = room_data['description']
        room.price = room_data['price']
        room.image = room_data['image']
        room.structure_id = room_data['structure_id']
        room.save()
        return Response("Room updated")
    else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def delete_room(request):
    user_id = request.data.get('owner_id')
    structure_id = request.data.get('structure_id')
    room_id = request.data.get('room_id')
    # Get structure
    structure = Structures.objects.filter(id = structure_id).first()
    if not structure or structure.owner_id is not user_id:
        raise exceptions.PermissionDenied("You cant perform this actions")
    # Get room
    room = StructureRooms.objects.filter(id = room_id).first()
    if not room or room.structure_id is not structure.id:
        raise exceptions.PermissionDenied("You cant perform this actions")
    # Perform delete
    room.delete()
    return Response("Room deleted!")

@api_view(['POST'])
def get_room_details(request):
    room_id = request.data.get('room_id')
    user_id = request.data.get('owner_id')
    # Get structure
    structures  = list(Structures.objects.filter(owner_id = user_id).values())
    structures_id = [structure['id'] for structure in structures]
    # Get room
    room = StructureRooms.objects.filter(id = room_id).values().first()
    # Check ownership
    if not room['structure_id'] in structures_id:
        raise exceptions.PermissionDenied("You cant perform this actions")
    return JsonResponse(room, safe=False)
    