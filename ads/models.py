from django.db import models
from accounts.models import User
from .utils import CATEGORIES
from django_resized import ResizedImageField

# Create your models here.
class Ad(models.Model):
    title = models.CharField(max_length=50)
    image = ResizedImageField(size=[500, 550], crop=['top', 'left'], upload_to='images/')
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads")

    def __str__(self):
        return self.title