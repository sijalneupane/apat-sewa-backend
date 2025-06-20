from django.contrib import admin
from .models import CustomUser
# Register your models here.

from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin
from .models import Place



admin.site.register(CustomUser)



@admin.register(Place)
class PlaceAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')
