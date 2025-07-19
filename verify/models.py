import email
from pyexpat import model
from django.db import models
from accounts.models import Person
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class OTP(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    email = models.EmailField(blank=False)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=5)

    def is_24_hour_passed(self):
        return self.created_at <= timezone.now() - timedelta(hours=24)
    
    
    def __str__(self):
        return f"{self.otp} - {self.user.email} - {self.user.username}"
    
    