from django.contrib.auth.decorators import login_required

import requests

# Create your views here.


@login_required
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        api_url = f"{request.scheme}://{request.get_host()}/api/sendOTP/"
        
        try:
            response = requests.post(api_url, json={'email': email})
            if response.status_code == 200:
                data = response.json()
                return JsonResponse({'message': data.get('message', 'OTP sent successfully.')})
            else:
                return JsonResponse({'error': 'Failed to send OTP.', 'details': response.text}, status=response.status_code)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while sending OTP.', 'details': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
    
# def verify_otp():
    
    