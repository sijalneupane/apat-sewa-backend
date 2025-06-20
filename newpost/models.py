from django.db import models

# Create your models here.
class UserPost(models.Model):
    description = models.TextField()
    image = models.CharField( max_length=255, blank=True, null=True)

class UnregisteredAlert(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField( max_length=255, blank=True, null=True)

class EmergencyAlertByUser(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='emergency_alerts')
    description = models.TextField()
    image = models.CharField( max_length=255, blank=True, null=True)

    