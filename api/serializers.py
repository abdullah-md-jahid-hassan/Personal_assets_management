from rest_framework import serializers
from accounts.models import Person
from django.contrib.auth.password_validation import validate_password


class loginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class registerSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        validate_password(value)
        return value

    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'password', 'nid', 'dob', 'gender',
            'area_present', 'city_present', 'country_present', 'area_permanent', 'city_permanent',
            'country_permanent', 'profile_photo'
        ]