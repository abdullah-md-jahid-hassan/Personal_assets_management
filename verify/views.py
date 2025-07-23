from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import requests

# Create your views here.

# @login_required
def verify_email(request):
    email = None
    otp_sent = False
    message = None
    error = None

    if request.method == 'POST':
        print(type(request.POST.get('send_otp')))
        email = request.POST.get('email')

        # Get access token from session
        access_token = request.session.get('access_token')
        headers = {}
        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'

        if request.POST.get('send_otp')=='1':
            print("I'm Here...!")
            # Build the API URL
            api_url = request.build_absolute_uri('/api/sendOTP/')
            response = requests.post(api_url, data={'email': email}, headers=headers)
            if response.status_code == 201:
                otp_sent = True
                message = response.json().get('message')
            else:
                error = response.json().get('message')

        elif request.POST.get('verify_otp')=='1':
            otp = request.POST.get('otp')
            otp_sent = True
            api_url = request.build_absolute_uri('/api/verifyOTP/')
            response = requests.post(api_url, data={'email': email, 'otp': otp}, headers=headers)
            if response.status_code == 200:
                message = response.json().get('message')
            else:
                error = response.json().get('message')

    context = {
        'otp_sent': otp_sent,
        'message': message,
        'error': error,
        'email': email,
    }
    return render(request, 'verify_email.html', context)
    
    
    
    