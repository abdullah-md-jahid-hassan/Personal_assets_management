from django.utils.http import urlencode
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse

import requests

def login_view(request):
    success_message = request.GET.get('success_message')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        stay_logged_in = request.POST.get('stay_logged_in') == 'on'
        
        # Use the API endpoint from api app
        root_url = request.build_absolute_uri('/')
        api_url = root_url + 'api/login/'
        
        # Prepare data for API
        data = {
            'username': username,
            'password': password
        }
        
        try:
            # Send POST request to API
            response = requests.post(api_url, json=data, timeout=10)
            
            if response.status_code == 200:
                # Login successful
                api_data = response.json()
                
                # Store tokens in session
                request.session['access_token'] = api_data.get('access')
                request.session['refresh_token'] = api_data.get('refresh')
                
                # Set session expiry based on "Stay Logged In" preference
                if stay_logged_in:
                    # 30 days for "Stay Logged In"
                    request.session.set_expiry(40 * 24 * 60 * 60)
                    request.session['stay_logged_in'] = True
                else:
                    # Default session expiry (usually 1 day)
                    request.session.set_expiry(1 * 24 * 60 * 60)  # Browser session
                    request.session['stay_logged_in'] = False
                
                # Return API data as JSON response
                # return redirect('dashboard')
                return JsonResponse(api_data)
            else:
                # Login failed
                return render(request, 'login.html', {'error': api_data.get('message')})
                
        except requests.exceptions.ConnectionError:
            # Connection error - API server not running
            error_message = "API server is not running. Please start the server and try again."
            return render(request, 'login.html', {'error': error_message})
        except requests.exceptions.Timeout:
            # Timeout error
            error_message = "Request timed out. Please try again."
            return render(request, 'login.html', {'error': error_message})
        except requests.RequestException as e:
            # Other network errors
            error_message = f"Connection error: {str(e)}"
            return render(request, 'login.html', {'error': error_message})
    
    # GET request - show login form
    return render(request, 'login.html', {'success_message': success_message})

def register_view(request):
    email = None
    password = None
    confirm_password = None
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        agree_terms = request.POST.get('agree_terms') == 'on'
        
        # Client-side validation
        if not all([email, password, confirm_password]):
            error_message = "All fields are required"
            return render(request, 'register.html', {'email': email, 'error': error_message})
        
        if password != confirm_password:
            error_message = "Passwords do not match"
            return render(request, 'register.html', {'email': email, 'error': error_message})
        
        if not agree_terms:
            error_message = "You must agree to the terms and conditions"
            return render(
                request,
                'register.html',
                {
                    'email': email,
                    'error': error_message
                })
        
        # Use the API endpoint from api app
        root_url = request.build_absolute_uri('/')
        api_url = root_url + 'api/register/'
        
        # Prepare data for API
        data = {
            'email': email,
            'password': password
        }
        
        try:
            # Send POST request to API
            response = requests.post(api_url, json=data, timeout=10)
            api_data = response.json()  # Always parse the response

            if response.status_code == 201:
                # Registration successful
                success_message = "Registration successful! Please log in."

                login_url = reverse('accounts:login')
                query_string = urlencode({'success_message': success_message})
                return redirect(f"{login_url}?{query_string}")
            
            return render(
                request,
                'register.html',
                {
                    'email': email,
                    'error': api_data.get('message')
                })
                
        except requests.exceptions.ConnectionError:
            # Connection error - API server not running
            error_message = "API server is not running. Please start the server and try again."
            return render(
                request,
                'register.html',
                {
                    'email': email,
                    'error': error_message
                })
            
        except requests.exceptions.Timeout:
            # Timeout error
            error_message = "Request timed out. Please try again."
            return render(
                request,
                'register.html',
                {
                    'email': email,
                    'error': error_message
                })
        except requests.RequestException as e:
            # Other network errors
            error_message = f"Connection error: {str(e)}"
            return render(
                request,
                'register.html',
                {
                    'email': email,
                    'error': error_message
                })
    
    # GET request - show registration form
    return render(
        request,
        'register.html',
        {
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        })

# for logout               
# Delete the token form session
# request.session.pop('access_token', None)
# request.session.pop('refresh_token', None)