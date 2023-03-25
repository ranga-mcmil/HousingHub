from django.shortcuts import render, get_object_or_404, redirect
from .models import House
from ads.models import Ad
from accounts.models import User
from django.contrib.auth.decorators import login_required
from .forms import HouseForm
from accounts.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notifications.signals import notify



# Create your views here.
def home(request):
    houses = House.objects.all().order_by('-date_created')
    ads = Ad.objects.all().order_by('-date_created')
    advertisers = User.objects.filter(user_type="ADVERTISER")

    context = {
        'houses': houses,
        'ads': ads,
        'advertisers': advertisers

    }
    return render(request, 'houses/home.html', context)


def houses(request):
    houses_list = House.objects.all().order_by('-date_created')

    page = request.GET.get('page', 1)
    paginator = Paginator(houses_list, 3)
    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        houses = paginator.page(1)
    except EmptyPage:
        houses = paginator.page(paginator.num_pages)

    context = {
        'houses': houses
    }
    return render(request, 'houses/houses.html', context)


def house(request, id):
    house = House.objects.get(id=id)
    booked_users = []
    for booking in house.bookings.all():
        booked_users.append(booking.user)

    print()
    context = {
        'house': house,
        'booked_users': booked_users
    }
    return render(request, 'houses/house.html', context)


@login_required()
def new(request):
    if request.method == 'POST':
        form = HouseForm(data=request.POST, files=request.FILES)
        users = User.objects.filter(user_type="TENANT")
        if form.is_valid():
            new_house = form.save()
            new_house.user = get_object_or_404(User, id=request.user.id)
            new_house.save()
            notify.send(request.user, recipient=users, verb='House', action_object=new_house, description=f'{request.user} created a house listing ')
            messages.success(request, "Saved successfully")
            return redirect('houses:house', new_house.id)
        messages.error(request, 'Form not valid')
    else:
        form = HouseForm()

    context = {
        'form': form,
        'title': "New"
    }

    return render(request, 'houses/new.html', context)


@login_required()
def edit(request, id):
    house = House.objects.get(id=id)

    if request.user == house.user:
        if request.method == 'POST':
            form = HouseForm(request.POST, instance=house, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes saved')
                return redirect('houses:house', house.id)
            messages.error(request, 'Error saving changes')
        else:
            form = HouseForm(instance=house)

        context = {
            'form': form,
            'house': house,
            'title': "Edit"
        }
        return render(request, 'houses/edit.html', context)
    else:
        return JsonResponse({'message': 'Not yours to edit '})


@login_required()
def delete(request, id):
    house = House.objects.get(id=id)

    if request.user == house.user:
        house.delete()
        messages.success(request, 'Successfully deleted')
    else:
        return JsonResponse({'message': 'Not yours to delete '})
    return redirect('houses:houses')