import random
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response, Serializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from .serializers import loginSerializer, registerSerializer, logoutSerializer, UserSerializer, OTPSerializer

from verify.models import OTP

from django.utils import timezone
from datetime import timedelta

from .email import send_email

from accounts.models import Person

import random





# Create your views here.
class RegisterView(APIView):
    serializer_class = registerSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for email duplication
        if Person.objects.filter(email=email).exists():
            return Response({'detail': 'Email already exists.'}, status=status.HTTP_409_CONFLICT)

        # Prepare data for serializer
        data = {
            'email': email,
            'username': email,
            'password': password
        }
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'email': email}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class LogoutView(APIView):
    serializer_class = logoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data['refresh']
                
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

class SendOTP(APIView):
    serializer_class = OTPSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the email from the request data
        request_email = request.data.get('email')
        
        # Check if the user's email is already verified
        if request.user.email == request_email and request.user.is_email_verified:
            return Response(
                {'message': 'Email is already verified'},
                status.HTTP_409_CONFLICT
            )
        
        # Count the number of OTP requests made by the user in the last 24 hours
        attempt_in_24_hours = OTP.objects.filter(
            user = request.user,
            created_at__gte = timezone.now() - timedelta(hours=24)
        ).count()

        # If the user has exceeded the daily OTP request limit, return a 429 response
        if attempt_in_24_hours >= 10:
            return Response(
                {'message': 'Too many requests for a day'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Generate a 6-digit random OTP
        otp = random.randint(100000, 999999)
        
        # Validate the email using the serializer (should be OTPSerializer)
        serializer = self.serializer_class(data={
            'user': request.user.id,
            'email': request_email,
            'otp': otp})

        if serializer.is_valid():
            # Create a new OTP object for the user
            if not serializer.save():
                return Response(
                    {'message': 'OTP Creation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Send email with subject and body
            subject = 'Verification OTP - Personal Asset Management'
            body = f"Your Verification OTP for the Email '{request_email}' is - {str(otp)}"
            send_email(subject, body, request_email)
            
            # Return a success response indicating OTP validity period
            return Response(
                {'message': 'OTP will be invalid after 5 minutes'},
                status=status.HTTP_201_CREATED
            )
        
        # If serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
# class verifyOTP(APIView):
#     serializer_class = OTPSerializer
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
#         user = request.user,
#         otp = request.get('otp')
#         serializer = self.serializer_class(data={
#             'user': user,
#             'otp': otp
#             })
        
#         if serializer.is_valid() and OTP.objects.filter(user = user, otp = otp):
            