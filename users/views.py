from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from newpost.views import register_device_token
# from users.models import User
from .serializers import LoginSerializer
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import make_password,check_password

User = get_user_model()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import CustomUser

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request) :
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            device_token = request.data.get('deviceToken', None)
            try:
                user = User.objects.get(phone_number=phone_number)
                if check_password(password, user.password):
                    # Use RefreshToken instead of AccessToken for better handling
                    # refresh = RefreshToken.for_user(user)
                    if device_token:
                         if not register_device_token(user, device_token):
                            raise Exception("Failed to register device")
                    access=AccessToken.for_user(user)
                    
                    # Add custom claims to the token
                    # refresh['email'] = user.email
                    # refresh['role'] = user.role
                    access['phone_number'] = user.phone_number
                    access['role'] = user.role
                    
                    return Response({
                        # "refresh": str(refresh),
                        "token": str(access),
                        "message": "Login Success",
                        "id":user.id,
                        "role":access.get('role'),
                        "fullname": user.full_name,
                        "phone_number": user.phone_number,
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            # except Exception as e:
            #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User updated successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Volunter
from .serializers import VolunterSerializer
# Create a volunteer
class VolunterCreateView(generics.CreateAPIView):
    queryset = Volunter.objects.all()
    serializer_class = VolunterSerializer
    permission_classes = [IsAuthenticated]

# List all volunteers
class VolunterListView(generics.ListAPIView):
    queryset = Volunter.objects.all()
    serializer_class = VolunterSerializer
    permission_classes = [IsAuthenticated]