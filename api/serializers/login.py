from rest_framework import serializers
from api.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    """Serializers login requests and logs in a exisiting user."""
    email = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=255)
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True,max_length=255, read_only=True)
    password = serializers.CharField(required=False, allow_blank=True, allow_null=True,max_length=128, write_only=True)
    token = serializers.CharField(required=False, allow_blank=True, allow_null=True,max_length=255, read_only=True)

    def validate(self, data):
        
        email = data.get('email', None)
        password = data.get('password', None)
        
        if not email:
            raise serializers.ValidationError("Invalid request required email")
        
        if not password :
            raise serializers.ValidationError("Invalid request required password")
        
        
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError('A user with this username and passowrd is not found')
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
            
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }