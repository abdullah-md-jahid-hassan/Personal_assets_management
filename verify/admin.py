from django.contrib import admin
from .models import OTP

# Register your models here.
@admin.register(OTP)
class AdminOTP(admin.ModelAdmin):
    list_display = ('user', 'email', 'is_24_hour_passed', 'is_valid', 'otp', 'created_at')
    search_fields = ('user', 'email', 'is_24_hour_passed')
    list_filter = ('created_at',)
    ordering = ('created_at',)