from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserUpdateForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from notifications.signals import notify
from django.views import generic
from django.contrib import messages
from .models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def accounts(request):
    advertisers_list = User.objects.filter(user_type="ADVERTISER")

    page = request.GET.get('page', 1)
    paginator = Paginator(advertisers_list, 3)
    try:
        advertisers = paginator.page(page)
    except PageNotAnInteger:
        advertisers = paginator.page(1)
    except EmptyPage:
        advertisers = paginator.page(paginator.num_pages)

    context = {
        'advertisers': advertisers
    }
    return render(request, 'accounts/accounts.html', context)


def account(request, id):
    advertiser = User.objects.get(id=id)

    try:
        ads = request.GET['ads']
    except:
        ads = None
    

    context = {
        'advertiser': advertiser,
        'ads': ads
    }
    
    return render(request, 'accounts/account.html', context)

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            messages.success(request, 'Account created successfully')
            return redirect('accounts:account', new_user.id)


    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/register.html', context)

@login_required
def edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes Saved Successfully")
            return redirect('accounts:account', request.user.id)
        messages.error(request, "Something happened")
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'accounts/edit.html', context)


@login_required()
def notifications_(request):
    user = request.user  
    user.notifications.unread().mark_all_as_read()
    notifications = user.notifications.read() 
    
    context = {
        'notifications': notifications
    }
    return render(request, 'accounts/notifications_.html', context)