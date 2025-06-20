from django.urls import path
from .views import UserPostCreateView, UnregisteredAlertCreateView, EmergencyAlertByUserCreateView

urlpatterns = [
    path('api/user-posts/', UserPostCreateView.as_view(), name='userpost-create'),
    path('api/unregistered-alerts/', UnregisteredAlertCreateView.as_view(), name='unregisteredalert-create'),
    path('api/emergency-alerts/', EmergencyAlertByUserCreateView.as_view(), name='emergencyalertbyuser-create'),
]
