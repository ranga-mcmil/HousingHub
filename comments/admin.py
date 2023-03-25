from django.contrib import admin
from .models import AdComment

# Register your models here.
@admin.register(AdComment)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'user_name_email', 'message', 'date_created', 'user')

