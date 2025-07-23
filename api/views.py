from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.contrib.auth import authenticate
from django.template.loader import render_to_string

from rest_framework.exceptions import NotAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import loginSerializer, registerSerializer, logoutSerializer, UserSerializer, OTPSerializer

from verify.models import OTP

from datetime import timedelta

from api.utility.email import SendEmail
from api.utility.verify import Verify_OTP

from accounts.models import Person

from django.core import signing
from django.core.signing import SignatureExpired, BadSignature

import random
import os





# Create your views here.
class RegisterView(APIView):
    serializer_class = registerSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for email duplication
        if Person.objects.filter(email=email, is_email_verified=True).exists():
            return Response({'message': 'Email already exists.'}, status=status.HTTP_409_CONFLICT)

        # Prepare data for serializer
        data = {
            'email': email,
            'username': email,
            'password': password
        }
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            if serializer.save():
                return Response({'email': email}, status=status.HTTP_201_CREATED)
            
        serializer_error = "\n--> ".join(
            str(error)
            for errors in serializer.errors.values()
            for error in errors
        )
        serializer_error = '-->' + serializer_error

        return Response({'message': serializer_error}, status=status.HTTP_400_BAD_REQUEST)

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
            
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    serializer_class = logoutSerializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if isinstance(exc, NotAuthenticated):
            return Response({'message': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data['refresh']
                
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
                
                return Response({
                    'message': 'Successfully logged out. Tokens have been blacklisted.'
                }, status=status.HTTP_200_OK)
            except TokenError:
                return Response({
                    'message': 'Invalid token provided.'
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

    def handle_exception(self, exc):
        if isinstance(exc, NotAuthenticated):
            return Response({'message': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)

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
                
            # Create verification link
            data = {'pk': request.user.pk, 'email': request_email, 'otp': otp}
            import os
            token = signing.dumps(data, salt=os.getenv('VERIFY_EMAIL_TOKEN_SALT', 'email_verification-link_slat'))
            verification_link = f"http://{request.get_host()}/api/VerifyEmailByLink/?token={token}"
            
            # Prepare Email credential
            subject = 'Verification OTP - Personal Asset Management'
            massage = f"Your Verification OTP for the Email '{request_email}' is - {str(otp)}"
            if verification_link:
                html_message = render_to_string('email_html.html', {'otp': otp, 'verification_link': verification_link})
            else:
                html_message = None
            
            # Send Email    
            SendEmail(
                subject,
                massage,
                request_email,
                html_message=html_message
            )
            
            # Return a success response indicating OTP validity period
            return Response(
                {'message': 'OTP will be invalid after 5 minutes'},
                status=status.HTTP_201_CREATED
            )
        
        # If serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class VerifyOTP(APIView):
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if isinstance(exc, NotAuthenticated):
            return Response({'message': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)

    def handle_exception(self, exc):
        from rest_framework.exceptions import NotAuthenticated
        if isinstance(exc, NotAuthenticated):
            return Response({'message': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)
    
    def post(self, request, *args, **kwargs):
        # Extract id, email and otp from the request data
        user_id = request.user.id
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        return Verify_OTP(user_id, email, otp)    
        
class VerifyOTPByLink(APIView):
    def get(self, request, *args, **kwargs):
        # GET token
        token = request.GET.get('token')
        
        try:
            # Decode the token
            data = signing.loads(
                token,
                salt=os.getenv('VERIFY_EMAIL_TOKEN_SALT', 'email_verification-link_slat'),
                max_age=300  # 5 minutes
            )
        except SignatureExpired:
            return Response({'message': 'Verification link has expired. Please request a new one.'}, status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({'message': 'Invalid verification link.'}, status.HTTP_400_BAD_REQUEST)
        return Verify_OTP(data['pk'], data['email'], data['otp'])
    