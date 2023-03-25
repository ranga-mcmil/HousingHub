from django.db import models
from ads.models import Ad
from bookings.models import Booking, Order
from accounts.models import User

# Create your models here.
class Payment(models.Model):
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="ad_payments", null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booking_payments", null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_payments", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    date_created = models.DateTimeField(auto_now_add=True)