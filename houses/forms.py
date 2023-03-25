from django import forms
from .models import House, Amenity
from .utils import CITIES, STATUS

class HouseForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'product_name',
            'placeholder': 'Address *',
            'class': 'form-control',
        }
    ))

    location = forms.ChoiceField(choices=CITIES, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'type',
        }
    ))

    price = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'price',
            'placeholder': 'Price *',
        }
    ))

    booking_fee = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'price',
            'placeholder': 'Booking Fee *',
        }
    ))


    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'description',
            'placeholder': 'Description *',
        }
    ))

    status = forms.ChoiceField(choices=STATUS, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'type',
        }
    ))

    beds_per_room = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'price',
        }
    ))

    baths_rooms = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'price'
        }
    ))

    girls_remaining_slots = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'price'
        }
    ))

    boys_remaining_slots = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'price'
        }
    ))

    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs = {
            'class': '',
        }),
        
    )
    

    image1 = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id': 'image',
            'class': 'form-control image-input',
        }
    ))

    image2 = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id': 'image2',
            'class': 'form-control image-input',
        }
    ))

    image3 = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id': 'image3',
            'class': 'form-control image-input',
        }
    ))

    class Meta:
       model = House
       fields = [
           'address', 'location', 'price', 'booking_fee', 'description', 
           'status', 'beds_per_room', 'baths_rooms', 'girls_remaining_slots',
            'boys_remaining_slots', 'amenities', 'image1', 'image2', 'image3'
       ]