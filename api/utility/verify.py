from django.shortcuts import render
from django.utils import timezone

import requests
from rest_framework import status
from rest_framework.response import Response

from datetime import timedelta

from django.db.models import deletion

from api.serializers import OTPSerializer

from verify.models import OTP
from accounts.models import Person

def Verify_OTP(id, email, otp):
    serializer_class = OTPSerializer
        
    # Validate input data using the serializer
    serializer = serializer_class(data={
        'user': id,
        'email': email,
        'otp': otp
    })

    # If serializer is not valid, return a 400 Bad Request with error message
    if not serializer.is_valid():
        return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)

    # Delete OTPs that are older than 24 hours to keep the table clean
    OTP.objects.filter(created_at__lte=timezone.now() - timedelta(hours=24)).delete()

    # Check if the OTP exists for the user and email
    otp_obj = OTP.objects.filter(user=id, email=email, otp=otp).first()
    if not otp_obj:
        # If OTP does not exist, return a 422 Unprocessable Entity
        return Response({'message': 'Wrong OTP, Please try again'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Check if the OTP is still valid (within 5 minutes)
    if not otp_obj.is_valid:
        return Response({'message': 'OTP expired, Please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the user's email and set is_email_verified to True
    if not Person.objects.filter(id=id).update(email=email, is_email_verified=True):
        # If update fails, return a 500 Internal Server Error
        return Response({'message': 'Failed to verify, please try again'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete the used OTP
    otp_obj.delete()

    return render(requests, 'email_verified.html', {'message': 'OTP verified'}, status=status.HTTP_200_OK)