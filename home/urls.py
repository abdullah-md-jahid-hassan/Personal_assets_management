from django.urls import path
from . import views

urlpatterns = [
    path('home.pam/', views.opening_page, name='home'),
]