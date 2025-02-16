from django import forms
from .models import Booking, ParkingSpacePhoto
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PhotosForm(forms.ModelForm):
    class Meta:
        model = ParkingSpacePhoto
        fields = ['image']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'start_time', 'end_time']

from django import forms
from .models import ParkingSpace

class ParkingSpaceForm(forms.ModelForm):
    PARKING_TYPE_CHOICES = [
        ('driveway', 'Driveway'),
        ('garage', 'Garage'),
        ('underground', 'Underground'),
        ('street_parking', 'Street Parking'),
    ]

    VEHICLE_SIZE_CHOICES = [
        ('compact', 'Compact'),
        ('standard', 'Standard'),
        ('large', 'Large'),
        ('oversized', 'Oversized'),
    ]

    address = forms.CharField(max_length=255, label='Address', widget=forms.TextInput(attrs={
        'placeholder': 'Enter street address',
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
    }))
    
    city = forms.CharField(max_length=100, label='City', widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
    }))
    
    zip_code = forms.CharField(max_length=20, label='ZIP Code', widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
    }))
    
    parking_type = forms.ChoiceField(choices=PARKING_TYPE_CHOICES, label='Parking Type', widget=forms.Select(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
    }))
    
    vehicle_size = forms.ChoiceField(choices=VEHICLE_SIZE_CHOICES, label='Vehicle Size', widget=forms.Select(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
    }))
    
    features = forms.MultipleChoiceField(
        choices=[
            ('24/7_access', '24/7 Access'),
            ('security_cameras', 'Security Cameras'),
            ('covered_parking', 'Covered Parking'),
            ('electric_charging', 'Electric Charging'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label='Features',
    )
    
    price_per_hour = forms.DecimalField(max_digits=10, decimal_places=2, label='Price per Hour', widget=forms.NumberInput(attrs={
        'placeholder': 'Enter price per hour',
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
    }))

    class Meta:
        model = ParkingSpace
        fields = ['address', 'city', 'zip_code', 'parking_type', 'vehicle_size', 'features', 'price_per_hour']       