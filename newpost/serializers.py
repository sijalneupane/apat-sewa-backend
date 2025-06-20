from rest_framework import serializers
from .models import UserPost, UnregisteredAlert, EmergencyAlertByUser
from users.models import CustomUser  # optional if you want to include user info

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['id', 'user', 'description', 'image']
        # if you want to show user details instead of just the ID, you can customize this

class UnregisteredAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnregisteredAlert
        fields = ['id', 'name', 'phone_number', 'description', 'image']

class EmergencyAlertByUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyAlertByUser
        fields = ['id', 'user', 'description', 'image']
