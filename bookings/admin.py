from django.contrib import admin
from .models import Booking, Order

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'house', 'user', 'date_created')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'ad', 'date_created')