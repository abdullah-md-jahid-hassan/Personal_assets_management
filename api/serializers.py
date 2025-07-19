from dataclasses import field
import email
import optparse
from pyexpat import model
from traceback import extract_stack
from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password

from accounts.models import Person
from verify.models import OTP


class registerSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Person(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = Person
        fields = [
            'email', 'username', 'password'
        ]
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True, 'write_only': True}
        }

class loginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class logoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        
class OTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    class Meta:
        model = OTP
        fields = ['user', 'email', 'otp']
        
        extra_kwargs = {
            'email': {'required': True}
        }
        
        