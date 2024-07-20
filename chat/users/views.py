from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
import logging


logger = logging.getLogger(__name__)
# Create your views here.
@login_required
def profile_page(request):
    return render(request, 'users/profile.html', {'profile_user': request.user})

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        logger.info(f"Login attempt for user: {username}")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            serializer = UserSerializer(user)
            logger.info(f"User {username} logged in successfully")
            return Response(serializer.data)
        logger.warning(f"Failed login attempt for user: {username}")
        return Response({
            'error': 'Invalid credentials',
            'details': {
                'username': username,
                'password_provided': bool(password)
            }
        }, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.accepted_renderer.format == 'html':
            return render(request, 'users/profile.html', {'profile_user': user})
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        if request.user.username != username:
            return Response({"error": "You can only update your own profile"}, status=status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, username=username)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    


class LoginStatusView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "status": "logged_in",
                "user": request.user.username
            })
        else:
            return Response({
                "status": "not_logged_in"
            })