from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad
from .forms import AdForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from comments.models import AdComment
from comments.forms import AdCommentForm
from accounts.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notifications.signals import notify
from payments.forms import PhoneNumberForm
from payments.ecocash import make_payment
from payments.forms import PhoneNumberForm
from bookings.models import Order
from payments.models import Payment


# Create your views here.
def ads(request):
    ads_list = Ad.objects.all().order_by('-date_created')

    page = request.GET.get('page', 1)
    paginator = Paginator(ads_list, 3)
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)


    context = {
        'ads': ads
    }
    return render(request, 'ads/ads.html', context)


def ad(request, id):
    ad = Ad.objects.get(id=id)
    if request.method != 'POST':
        form = AdCommentForm()
        comments = ad.ad_comments.all()
        
    else:
        form = AdCommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.ad = ad
            if request.user.is_authenticated:
                user = get_object_or_404(User, id=request.user.id)
                new_comment.user_name = user.get_full_name()
                new_comment.user_name_email = user.email
                new_comment.user = user
            new_comment.save()
            notify.send(request.user, recipient=ad.user, verb='Ad', action_object=ad, description=f'{request.user} commented to your ad')
            messages.success(request, "comment sent")
            return redirect(request.META['HTTP_REFERER'])
        messages.error(request, 'Form not valid')

    context = {
        'ad': ad,
        'comments': comments,
        'form': form
    }
    return render(request, 'ads/ad.html', context)

@login_required()
def new(request):
    if request.method == 'POST':
        form = AdForm(data=request.POST, files=request.FILES)
        ecocash_form = PhoneNumberForm(request.POST)

        if form.is_valid() and ecocash_form.is_valid():
            phone_number = ecocash_form.get_info()

            new_ad = form.save(commit=False)
            new_ad.user = get_object_or_404(User, id=request.user.id)
            # payment_status = make_payment(f'New Ad ', phone_number, request.user.email, 1)['status']
            payment_status = 'paid'
            if payment_status == 'paid':
                new_ad.save()
                Payment.objects.create(
                    amount=1,
                    ad=new_ad,
                    user=request.user
                )
                messages.success(request, "Uploaded successfully")
                return redirect('ads:ad', new_ad.id)
            
            elif payment_status == 'sent':
                messages.error(request, 'Ecocash prompt sent, could not get confirmation from user. Please try again')
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, 'Error happened, please try again')
                return redirect(request.META['HTTP_REFERER'])

        messages.error(request, 'Form not valid')
    else:
        form = AdForm()
        ecocash_form = PhoneNumberForm()


    context = {
        'form': form,
        'title': "New",
        'ecocash_form': ecocash_form
    }

    return render(request, 'ads/new.html', context)

@login_required()
def edit(request, id):
    ad = Ad.objects.get(id=id)

    if request.user == ad.user:
        if request.method == 'POST':
            form = AdForm(request.POST, instance=ad, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes saved')
                return redirect('ads:ad', ad.id)
            messages.error(request, 'Error saving changes')
        else:
            form = AdForm(instance=ad)

        context = {
            'form': form,
            'ad': ad,
            'title': "Edit"
        }
        return render(request, 'ads/edit.html', context)
    else:
        return JsonResponse({'message': 'Not yours to edit '})



@login_required()
def delete(request, id):
    ad = Ad.objects.get(id=id)

    if request.user == ad.user:
        ad.delete()
        messages.success(request, 'Ad successfully deleted')
    else:
        return JsonResponse({'message': 'Not yours to delete '})
    return redirect('ads:ads')


@login_required()
def order_item(request, id):
    ad = Ad.objects.get(id=id)
    if request.method != 'POST':
        form = PhoneNumberForm()
    else:
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.get_info()

            # payment_status = make_payment(f'Order for Ad - ID({ad.id})', phone_number, request.user.email, 1)['status']
            payment_status = 'paid'
            if payment_status == 'paid':
                new_order = Order.objects.create(amount=ad.price, ad=ad, user=request.user)
                Payment.objects.create(
                    amount=new_order.amount,
                    order=new_order,
                    user=request.user
                )
                notify.send(request.user, recipient=ad.user, verb='Order', action_object=ad, description=f'{request.user} ordered your item ')
                messages.success(request, 'Order was successful')
                
                return redirect('ads:ad', ad.id)
                
            elif payment_status == 'sent':
                messages.error(request, 'Ecocash prompt sent, could not get confirmation from user. Please try again')
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, 'Error happened, please try again')
                return redirect(request.META['HTTP_REFERER'])


    context = {
        'form': form, 
        'ad': ad
    }
    return render(request, 'ads/order_item.html', context)

@login_required()
def orders(request, id):
    ad = Ad.objects.get(id=id)

    context = {
        'ad': ad
    }
    
    return render(request, 'ads/orders.html', context)