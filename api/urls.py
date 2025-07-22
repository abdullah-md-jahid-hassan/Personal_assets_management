from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='Login API'),
    path('register/', views.RegisterView.as_view(), name='Register API'),
    path('logout/', views.LogoutView.as_view(), name='Logout API'),
    path('dashboard/', views.DashboardView.as_view(), name='Dashboard API'),
    path('sendOTP/', views.SendOTP.as_view(), name='Send OTP API'),
    path('verifyOTP/', views.VerifyOTP.as_view(), name='Verify OTP API'),
    path('VerifyEmailByLink/', views.VerifyOTPByLink.as_view(), name='Verify OTP By Email API'),
    path('get-access-by-refresh/', TokenRefreshView.as_view(), name='Token_refresh API'),
]