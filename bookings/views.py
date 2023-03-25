from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from houses.models import House
from accounts.models import User
from payments.forms import PhoneNumberForm
from .forms import GenderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from notifications.signals import notify
from payments.ecocash import make_payment
from django.core.mail import send_mail
from django.conf import settings
from payments.models import Payment

@login_required()
def new(request, id):
    house = House.objects.get(id=id)
    if request.method != 'POST':
        form = PhoneNumberForm()
        gender_form = GenderForm()
    else:
        form = PhoneNumberForm(request.POST)
        gender_form = GenderForm(request.POST)
        if form.is_valid() and gender_form.is_valid():
            phone_number = form.get_info()
            gender = gender_form.get_info()

            if gender == 'Boy' and house.boys_remaining_slots == 0:
                messages.error(request, 'Sorry, no rooms for boys left')
                return redirect(request.META['HTTP_REFERER'])

            if gender == 'Girl' and house.girls_remaining_slots == 0:
                messages.error(request, 'Sorry, no rooms for girls left')
                return redirect(request.META['HTTP_REFERER'])


            # payment_status = make_payment(f'House Booking - ID({house.id})', phone_number, request.user.email, 1)['status']
            payment_status = 'paid'
            if payment_status == 'paid':
                new_booking = Booking.objects.create(house=house, user=request.user, fee=house.booking_fee)
                if gender == "Girl":
                    house.girls_remaining_slots -=1
                else:
                    house.boys_remaining_slots -=1
                house.save()
                Payment.objects.create(
                    amount=house.booking_fee,
                    booking=new_booking,
                    user=request.user
                )
                
                notify.send(request.user, recipient=house.user, verb='Booking', action_object=house, description=f'{request.user} booked a room ')
                messages.success(request, 'Booked successfuly')
                
                return redirect('houses:house', house.id)
                
            elif payment_status == 'sent':
                messages.error(request, 'Ecocash prompt sent, could not get confirmation from user. Please try again')
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, 'Error happened, please try again')
                return redirect(request.META['HTTP_REFERER'])


    context = {
        'form': form, 
        'gender_form': gender_form,
        'house': house
    }
    
    return render(request, 'bookings/new.html', context)


@login_required()
def booked(request, id):
    house = House.objects.get(id=id)

    context = {
        'house': house
    }
    
    return render(request, 'bookings/booked.html', context)