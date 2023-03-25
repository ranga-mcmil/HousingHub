from django.urls import path
from . import views


app_name = 'ads'
urlpatterns = [
   path('', views.ads, name='ads'),
   path('<int:id>', views.ad, name='ad'),
   path('new/', views.new, name='new'),
   path('delete/<int:id>', views.delete, name='delete'),
   path('edit/<int:id>/', views.edit, name='edit'),
   path('order_item/<int:id>/', views.order_item, name='order_item'),
   path('orders/<int:id>/', views.orders, name='orders'),
   

]