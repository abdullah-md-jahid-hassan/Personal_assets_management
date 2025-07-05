from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Person, Admin, User_client

# Register your models here.

@admin.register(Person)
class PersonAdmin(UserAdmin):
    """Admin configuration for the Person model"""
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'nid', 'gender', 'dob')}),
        (('Present Address'), {'fields': ('area_present', 'city_present', 'country_present')}),
        (('Permanent Address'), {'fields': ('area_permanent', 'city_permanent', 'country_permanent')}),
        (('User Type'), {'fields': ('type', 'profile_photo')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'type', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('type', 'is_staff', 'is_superuser')
    ordering = ('-date_joined',)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    """Admin configuration for the Admin model"""
    list_display = ('person', 'role', 'designation', 'joining_date')
    search_fields = ('person__email', 'person__first_name', 'person__last_name', 'role', 'designation')
    list_filter = ('role',)


@admin.register(User_client)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for the User model"""
    list_display = ('person', 'registration_date')
    search_fields = ('person__email', 'person__first_name', 'person__last_name', 'person__phone')
    list_filter = ('registration_date',)
