from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm
from accounts.views import LoginView

app_name = 'accounts'
urlpatterns = [
   path('', views.accounts, name='accounts'),
   path('<int:id>/', views.account, name='account'),   
   path('login/', auth_views.LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('register/', views.register, name='register'),
   path('edit/', views.edit, name='edit'), 
   path('notifications_/', views.notifications_, name='notifications_'),
   

]