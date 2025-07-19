from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

def login_view(request):
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
                    request.session.set_expiry(40 * 24 * 60 * 60)  # 30 days in seconds
                    request.session['stay_logged_in'] = True
                else:
                    # Default session expiry (usually 2 weeks)
                    request.session.set_expiry(40 * 24 * 60 * 60)  # Browser session
                    request.session['stay_logged_in'] = False
                
                # Return API data as JSON response
                # return redirect('dashboard')
                return JsonResponse(api_data)
            else:
                # Login failed
                error_message = "Invalid username or password"
                return render(request, 'login.html', {'error': error_message})
                
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
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        agree_terms = request.POST.get('agree_terms') == 'on'
        
        # Client-side validation
        if not all([email, username, password, confirm_password]):
            error_message = "All fields are required"
            return render(request, 'register.html', {'error': error_message})
        
        if password != confirm_password:
            error_message = "Passwords do not match"
            return render(request, 'register.html', {'error': error_message})
        
        if not agree_terms:
            error_message = "You must agree to the terms and conditions"
            return render(request, 'register.html', {'error': error_message})
        
        # Use the API endpoint from api app
        root_url = request.build_absolute_uri('/')
        api_url = root_url + 'api/register/'
        
        # Prepare data for API
        data = {
            'email': email,
            'username': username,
            'password': password
        }
        
        try:
            # Send POST request to API
            response = requests.post(api_url, json=data, timeout=10)
            
            if response.status_code == 201:
                # Registration successful
                api_data = response.json()
                
                # Store tokens in session
                request.session['access_token'] = api_data.get('access')
                request.session['refresh_token'] = api_data.get('refresh')
                
                # Return API data as JSON response
                # return redirect('dashboard')
                return JsonResponse(api_data)
                
            elif response.status_code == 400:
                # Registration failed - validation errors
                api_data = response.json()
                error_message = api_data.get('detail', 'Registration failed. Please check your information.')
                return render(request, 'register.html', {'error': error_message})
                
            else:
                # Other errors
                error_message = "Registration failed. Please try again."
                return render(request, 'register.html', {'error': error_message})
                
        except requests.exceptions.ConnectionError:
            # Connection error - API server not running
            error_message = "API server is not running. Please start the server and try again."
            return render(request, 'register.html', {'error': error_message})
        except requests.exceptions.Timeout:
            # Timeout error
            error_message = "Request timed out. Please try again."
            return render(request, 'register.html', {'error': error_message})
        except requests.RequestException as e:
            # Other network errors
            error_message = f"Connection error: {str(e)}"
            return render(request, 'register.html', {'error': error_message})
    
    # GET request - show registration form
    return render(request, 'register.html')

# for logout               
# Delete the token form session
# request.session.pop('access_token', None)
# request.session.pop('refresh_token', None)