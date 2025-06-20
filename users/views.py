from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
# from users.models import CustomUser
from .serializers import UserCreateSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully.",
                "user": UserCreateSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except user.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response({'error': 'Invalid Passsword'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = AccessToken.for_user(user)
        return Response({
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)



from rest_framework.permissions import IsAuthenticated, IsAdminUser
class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully.",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from .models import Place
from django.contrib.gis.geos import Point

p = Place(name="Kathmandu", location=Point(85.3240, 27.7172))  # (longitude, latitude)
p.save()


from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D  # 'D' is a shortcut for Distance units

# Example user location (Kathmandu)
user_location = Point(85.3240, 27.7172, srid=4326)  # Always set SRID!

# Places within 10 km
places_within_5km = Place.objects.filter(
    location__distance_lte=(user_location, D(km=5))
).annotate(
    distance=Distance('location', user_location)
).order_by('distance')

for place in places_within_5km:
    print(place.name, place.distance.km)  # distance in kilometers