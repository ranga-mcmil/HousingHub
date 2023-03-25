from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
   path('<int:id>/', views.booked, name='booked'),
   path('new/<int:id>/', views.new, name='new'),

   
]