from django.db import models
from accounts.models import User
from .utils import CITIES, STATUS
from django_resized import ResizedImageField

class Amenity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Create your models here.
class House(models.Model):
    address = models.CharField(max_length=50)
    location = models.CharField(max_length=50, choices=CITIES)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    booking_fee = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=50, choices=STATUS)
    beds_per_room = models.IntegerField(default=0)
    baths_rooms = models.IntegerField(default=0)
    girls_remaining_slots = models.IntegerField(default=0)
    boys_remaining_slots = models.IntegerField(default=0)
    amenities = models.ManyToManyField(Amenity, null=True, blank=True)
    image1 = ResizedImageField(size=[500, 550], crop=['top', 'left'], upload_to='images/')
    image2 = ResizedImageField(size=[500, 550], crop=['top', 'left'], upload_to='images/')
    image3 = ResizedImageField(size=[500, 550], crop=['top', 'left'], upload_to='images/')
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="houses", null=True, blank=True)

    def __str__(self):
        return f'{self.address}, {self.location}'

    def get_slots_available(self):
        return self.girls_remaining_slots + self.boys_remaining_slots

    def split_address(self):
        
        return self.address.split(' ')[0]

    def split_address_second(self):
        
        return ' '.join(map(str, self.address.split(' ')[1:]))
        