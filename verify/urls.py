from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('SendOTP/', views.send_otp, name='Send OTP'),
    # path('VerifyOTP/', views.verify_otp, name='Verify OTP'),
]