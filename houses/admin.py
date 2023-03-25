from django.contrib import admin
from .models import House, Amenity

# Register your models here.
@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('address', 'location', 'price', 'status', 'date_created')

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)