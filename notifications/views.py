from django.shortcuts import render
from .models import NotificationRequest, NotificationList
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(['POST'])
def create_notification_request(request):
    # Check if there's already a notification
    check = NotificationRequest.objects.filter(
            user_id = request.data.get('user_id'),
            structure_id = request.data.get('structure_id'),
            date_from = request.data.get('date_from'),
            date_to = request.data.get('date_to')
        ).count()
    if check > 0:
        return Response("You already submitted a similar request!")
    # Otherwise create it
    notification_request = NotificationRequest()
    notification_request.user_id = request.data.get('user_id')
    notification_request.structure_id = request.data.get('structure_id')
    notification_request.date_from = request.data.get('date_from')
    notification_request.date_to = request.data.get('date_to')
    notification_request.save()
    return Response("We will notify you if a place becomes available")

@api_view(['POST'])
def notification_list(request):
    user_id = request.data.get('user_id')
    notifications = list(NotificationList.objects.filter(user_id = user_id).values())
    for notification in notifications:
        # Update read Clause
        if not notification['read']:
            tmp_notification = NotificationList.objects.filter(id = notification['id']).first()
            tmp_notification.read = 1
            tmp_notification.save()
    # Return
    return JsonResponse(notifications, safe=False)

@api_view(['POST'])
def check_user_notifications(request):
    user_id = request.data.get('user_id')
    notifications = list(NotificationList.objects.filter(user_id = user_id, read = False).values())
    # Return
    return Response(len(notifications) > 0)
