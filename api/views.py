from http.client import HTTPResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import loginSerializer, registerSerializer, logoutSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from .email import send_email



# Create your views here.
class LoginView(APIView):
    serializer_class = loginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Generate JWT token using Simple JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    serializer_class = registerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    serializer_class = logoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data['refresh']
                access_token = serializer.validated_data['access']
                
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
                
                return Response({
                    'detail': 'Successfully logged out. Tokens have been blacklisted.'
                }, status=status.HTTP_200_OK)
            except TokenError:
                return Response({
                    'detail': 'Invalid token provided.'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_type = request.user.type
        if user_type == 'admin':
            return Response({
                'detail': 'Admin dashboard view'
            }, status=status.HTTP_200_OK)
        elif user_type == 'user':
            serializer = UserSerializer(request.user)
            return Response({
                'detail': 'User dashboard view',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'detail': 'invalid user'
        }, status=status.HTTP_401_UNAUTHORIZED)


# class SendOTP(APIView):
#     def post(self, request, *args, **kwargs):
        


