from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class Person(AbstractUser):
    """Custom user model that extends Django's AbstractUser"""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'), 
    )
    
    # Personal information - made optional for easier registration
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    nid = models.CharField(max_length=20, verbose_name='National ID', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(verbose_name='Date of Birth', blank=True, null=True)
    
    # Present address - made optional
    area_present = models.CharField(max_length=255, blank=True, null=True)
    city_present = models.CharField(max_length=100, blank=True, null=True)
    country_present = models.CharField(max_length=100, blank=True, null=True)
    
    # Permanent address - made optional
    area_permanent = models.CharField(max_length=255, blank=True, null=True)
    city_permanent = models.CharField(max_length=100, blank=True, null=True)
    country_permanent = models.CharField(max_length=100, blank=True, null=True)
    
    # User type and profile photo
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} - {self.type}"
        return f"{self.username} - {self.type}"

    # Only username and password are required for registration
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # If first_name and last_name are not provided, set first_name to username
        if not self.first_name and not self.last_name:
            self.first_name = self.username
        super().save(*args, **kwargs)

class Admin(models.Model):
    """Admin model that extends Person model"""
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('moderator', 'Moderator'),
    )
    
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()
    
    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} - {self.get_role_display()}"


class User_client(models.Model):
    """User model that extends Person model"""
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    registration_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name}"






