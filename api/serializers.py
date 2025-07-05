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
            'password': {'required': True, 'write_only': True}
        }