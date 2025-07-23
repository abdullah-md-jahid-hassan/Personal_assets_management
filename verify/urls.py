from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('verify_email/', views.verify_email, name='verify_email'),
]