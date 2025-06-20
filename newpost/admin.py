from django.contrib import admin
from .models import UnregisteredAlert, UserPost, EmergencyAlertByUser
# Register your models here.

admin.site.register(UnregisteredAlert)
admin.site.register(UserPost)  
admin.site.register(EmergencyAlertByUser)