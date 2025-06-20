# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework import serializers
from .models import CustomUser
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'full_name', 'password']
        extra_kwargs = {
            'email': {'required': False},
            'phone_number': {'required': False},
            'full_name': {'required': False},
            'password': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

# class UserLoginSerializer(serializers.Serializer):
#     phone_number = serializers.CharField(required=True)
#     password = serializers.CharField(write_only=True, required=True, min_length=8)

class LoginSerializer(serializers.Serializer):
    deviceToken = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if not phone_number or not password:
            raise serializers.ValidationError("Both contact and password and device token are required.")

        return attrs
    
# serializers.py
from rest_framework import serializers
from .models import Volunter

class VolunterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunter
        fields = ['id', 'user', 'email', 'skill']
