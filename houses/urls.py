from django.urls import path
from . import views


app_name = 'houses'
urlpatterns = [
   path('', views.home, name='home'),
   path('houses/', views.houses, name='houses'),
   path('house/<int:id>/', views.house, name='house'),
   path('house/new/', views.new, name='new'),
   path('house/delete/<int:id>/', views.delete, name='delete'),
   path('house/edit/<int:id>/', views.edit, name='edit'),

]