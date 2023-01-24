from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterUserSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet
import requests

class RegisterUserView(CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer

@api_view(['POST'])
def login(request):
    # Get data
    email = request.data.get('email')
    password = request.data.get('password')
    # Validate users
    user = get_user_model().objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed("Email or password missmatch")
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("Email or password missmatch")
    # Get the token endpoint and request tokens
    token_endpoint = reverse(viewname='token_obtain_pair', request=request)
    tokens = requests.post(token_endpoint, data=request.data).json()
    # Generate response object and return it
    response = Response()
    response.data = {
        'access_token': tokens.get('access'),
        'refresh_token': tokens.get('refresh'),
        'username': user.username
    }
    return response

class CurrentLoggedInUser(ModelViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        user_profile = self.queryset.get(email=request.user.email)
        serializer = self.get_serializer(user_profile)
        return Response({'user': serializer.data})

@api_view(['POST'])
def update_user_settings(request):
    # Get data
    id = request.data.get('id')
    user = get_user_model().objects.filter(id=id).first()
    if user is None:
        raise exceptions.PermissionDenied("Somethings went wrong")
    # Email
    email = request.data.get('email')
    if email and email != user.email:
        user.email = email
    # Check passwords
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if old_password and new_password:
        if not user.check_password(old_password):
            raise exceptions.AuthenticationFailed("Old password missmatch")
        user.set_password(new_password)
    # Avatar
    avatar = request.data.get('avatar')
    if avatar:
        # Update
        user.avatar = avatar
    # Username
    username = request.data.get('username')
    if username:
        user.username = username
    # Update
    user.save()
    return Response("User settings updated")