from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserPost, UnregisteredAlert, EmergencyAlertByUser
from .serializers import UserPostSerializer, UnregisteredAlertSerializer, EmergencyAlertByUserSerializer
from users.models import CustomUser

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
