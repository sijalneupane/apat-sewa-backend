from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserPost, UnregisteredAlert, EmergencyAlertByUser
from .serializers import UserPostSerializer, UnregisteredAlertSerializer, EmergencyAlertByUserSerializer
from users.models import CustomUser
from .models import CustomDevice

class UserPostCreateView(APIView):
    def post(self, request):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnregisteredAlertCreateView(APIView):
    def post(self, request):
        serializer = UnregisteredAlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmergencyAlertByUserCreateView(APIView):
    def post(self, request):
        serializer = EmergencyAlertByUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def register_device_token( user, device_token):
    """
    Register a device token for the authenticated user.
    Allows multiple devices per user.
    """
    # # Explicitly set renderer classes if needed
    # request.accepted_renderer = JSONRenderer()
    """
    Register a device token for the authenticated user.
    Allows multiple devices per user.
    """
    # device_token = data.get('deviceToken')
    # device_type = request.data.get('deviceType', 'android')  # default to android
    try:  
        if not device_token:
            return False

        # Check if user has existing devices
        existing_devices = CustomDevice.objects.filter(user=user, active=True)
        device_count = existing_devices.count()

        # If user has exactly one device, update its registration_id
        if device_count == 1:
            existing_device = existing_devices.first()
            existing_device.registration_id = device_token
            existing_device.save()
            return True

        # Otherwise, use the original get_or_create logic
        device, created = CustomDevice.objects.get_or_create(
            registration_id=device_token,
            defaults={
                'user': user,
                'active': True,
            }
        )
        
        if not created:
            # If device already exists, update user and set active
            device.user = user
            device.active = True
            device.save()

        return True
        
    except Exception as e:
        # Note: This will cause an error since Response is not imported
        # Consider returning False or logging the error instead
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)