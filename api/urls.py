from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('sendOTP/', views.SendOTP.as_view(), name='Send OTP'),
    path('get-access-by-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]