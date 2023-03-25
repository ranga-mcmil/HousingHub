from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django_resized import ResizedImageField



# Create your models here.
class User(AbstractUser):

    class Types(models.TextChoices):
        ADVERTISER = "ADVERTISER", "ADVERTISER"
        TENANT = "TENANT", 'TENANT'

    # Type of user
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(_('Type'), max_length=50, choices=Types.choices)
    contact_number = models.CharField(max_length=250, unique=True)
    pic = ResizedImageField(size=[500, 550], crop=['top', 'left'], upload_to='images/')
    bio = models.TextField(max_length=50)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)
