from django.db import models
from fcm_django.models import AbstractFCMDevice


# Create your models here.
class UserPost(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='posts')
    description = models.TextField()
    image = models.CharField( max_length=255, blank=True, null=True)
     
    def __str__(self):
        return f"Post {self.id} - {self.description[:20]}"

class UnregisteredAlert(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField( max_length=255, blank=True, null=True)
    def __str__(self):
        return f"Alert by {self.name} - {self.description[:20]}"

class EmergencyAlertByUser(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='emergency_alerts')
    description = models.TextField()
    image = models.CharField( max_length=255, blank=True, null=True)

    
class CustomDevice(AbstractFCMDevice):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)