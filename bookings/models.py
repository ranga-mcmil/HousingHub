from django.db import models
from houses.models import House
from accounts.models import User
from ads.models import Ad

# Create your models here.
class Booking(models.Model):
    fee = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookings")
    date_created = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="orders")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    date_created = models.DateTimeField(auto_now_add=True)