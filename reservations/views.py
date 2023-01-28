from django.shortcuts import render
from .models import Reservations
from structures.models import Structures
from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
from rest_framework import exceptions

@api_view(['POST'])
def create_reservation(request):
    reservation = Reservations()
    reservation.user_id = request.data.get('user')
    reservation.structure_id = request.data.get('structure')
    reservation.date_from = request.data.get('date_from')
    reservation.date_to = request.data.get('date_to')
    reservation.save()
    return Response("Reservetion submitted!")

@api_view(['POST'])
def get_user_reservation(request):
    user_id = request.data.get('user_id')
    if user_id:
        # Get reservation for the user
        reservations =  list(Reservations.objects.filter(user_id = user_id).values())
        skip_structure = False
    else:
        # Get owner info
        owner_id = request.data.get('owner_id')
        structure_id = request.data.get('structure_id')
        # Structure 
        structure = Structures.objects.filter(id = structure_id).first()
        if structure.owner_id is owner_id:
            reservations =  list(Reservations.objects.filter(structure_id = structure_id).values())
            skip_structure = True
        else:
            raise exceptions.PermissionDenied("You cant perform this action")
    # Create clean list
    reservation_list = []
    for reservation in reservations:
        tmp_reservation = {}
        tmp_reservation['id'] = reservation['id']
        # If can skip structure info, staff is authenticathed
        if not skip_structure:
            structure = Structures.objects.filter(id = reservation['structure_id']).first()
            tmp_reservation['structure'] = structure.name
            tmp_reservation['address'] = f"{structure.city} - {structure.address}"
        else:
            user = User.objects.filter(id = reservation['user_id']).first()
            tmp_reservation['user'] = user.email
        # Period
        tmp_reservation['period'] = f"{reservation['date_from']} - {reservation['date_to']}"
        # Can canel
        if datetime.today().date() < reservation['date_from']:
            tmp_reservation['can_cancel'] = True
        else:
            tmp_reservation['can_cancel'] = False
        # Append to list
        reservation_list.append(tmp_reservation)
    # Return
    return JsonResponse(reservation_list, safe=False)

@api_view(['POST'])
def delete_reservation(request):
    # Retrieve reservation
    reservation_id = request.data.get('reservation_id')
    reservation = Reservations.objects.filter(id = reservation_id).first()
    # Check if user
    user_id = request.data.get('user_id')
    if user_id:
        if reservation.user_id is user_id:
            reservation.delete()
            return Response("Reservetion deleted!")
        else:
            raise exceptions.PermissionDenied("You cant perform this action")
    # Check if owner
    owner_id = request.data.get('owner_id')
    if owner_id:
        structure = Structures.objects.filter(id = reservation_id.structure_id).first()
        if structure.owner_id is owner_id:
            reservation.delete()
            return Response("Reservetion deleted!")
        else:
            raise exceptions.PermissionDenied("You cant perform this action")
    # Else raise exception
    raise exceptions.PermissionDenied("You cant perform this action")