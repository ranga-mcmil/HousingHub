from django.shortcuts import render, get_object_or_404, redirect
from ads.models import Ad
from houses.models import House
from accounts.models import User
from .forms import SearchForm
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse



# Create your views here.
def search(request):
    if request.method == 'POST':
        print("Got the data")
        form = SearchForm(request.POST)
        if form.is_valid():
            search_val = form.get_info()
            return redirect(reverse('search:search') + f'?search={search_val}')

    else:
        try:
            search_val = request.GET['search']
        except:
            messages.error(request, 'Error occured')
            return redirect(request.META['HTTP_REFERER'])

        ads = Ad.objects.filter(Q(title__icontains=search_val))
        houses = House.objects.filter(Q(address__icontains=search_val) | Q(location__icontains=search_val))
        advertisers = User.objects.filter(Q(first_name__icontains=search_val) | Q(last_name__icontains=search_val)).order_by('?')
        


       

        print(ads)
        print(houses)
        print(advertisers)

        context = {
            'ads': ads,
            'houses': houses,
            'advertisers': advertisers
        }

        return render(request, 'search/search.html', context)