from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

# Custom user manager
# This is used to create a custom user manager for the Person model
# It is used to create a custom user manager for the Person model
# It is used to create a custom user manager for the Person model 
class PersonManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('username', email)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

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
    
    # Personal information
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    nid = models.CharField(max_length=20, verbose_name='National ID')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(verbose_name='Date of Birth')
    
    # Present address
    area_present = models.CharField(max_length=255)
    city_present = models.CharField(max_length=100)
    country_present = models.CharField(max_length=100)
    
    # Permanent address
    area_permanent = models.CharField(max_length=255)
    city_permanent = models.CharField(max_length=100)
    country_permanent = models.CharField(max_length=100)
    
    # User type and profile photo
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    profile_photo = models.ImageField(upload_to='profile_photos/')
    
    objects = PersonManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.type}"

    REQUIRED_FIELDS = ['first_name', 'last_name', 'nid', 'dob', 'area_present', 'city_present', 'country_present', 'area_permanent', 'city_permanent', 'country_permanent']

    def save(self, *args, **kwargs):
        # Ensure username is always set to email
        self.username = self.email
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






