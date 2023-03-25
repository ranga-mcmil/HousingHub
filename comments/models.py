from django.db import models
from ads.models import Ad
from accounts.models import User

# Create your models here.
class AdComment(models.Model):
    user_name = models.CharField(max_length=200)
    user_name_email = models.CharField(max_length=200)
    message = models.TextField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="ad_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)