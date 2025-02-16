from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ParkingSpace, Booking
from .forms import BookingForm

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to home page
    else:
        form = RegisterForm()
    return render(request, 'parking/authentications.html', {'form': form, 'tab': 'register'})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to home page
    else:
        form = LoginForm()
    return render(request, 'parking/authentications.html', {'form': form, 'tab': 'login'})


def listingpage(request):
    return render(request, 'parking/listingpage.html')

def addphotos(request):
    return render(request, 'parking/addphotos.html')


from django.shortcuts import render, redirect
from .forms import PhotosForm
from .models import Photos

def upload_photos(request):
    if request.method == 'POST':
        form = PhotosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('setpricing')  # Redirect to a success page or another view
    else:
        form = PhotosForm()
    return render(request, 'parking/addphotos.html', {'form': form})

def setpricing(request):
    return render(request, 'parking/setpricing.html')  # Create a success.html template to show a success message

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    parking_spaces = ParkingSpace.objects.filter(available=True)
    return render(request, 'parking/home.html', {'parking_spaces': parking_spaces})

def search_results(request):
    query = request.GET.get('q', '')
    parking_spaces = ParkingSpace.objects.filter(location__icontains=query)
    return render(request, 'parking/searchresult.html', {'parking_spaces': parking_spaces, 'query': query})

def result_details(request, id):
    parking_space = get_object_or_404(ParkingSpace, id=id)
    return render(request, 'parking/resultdetails.html', {'parking_space': parking_space})

@login_required
def payment(request, id):
    parking_space = get_object_or_404(ParkingSpace, id=id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.parking_space = parking_space
            booking.total_amount = parking_space.price_per_hour * (booking.end_time.hour - booking.start_time.hour)
            booking.save()
            return redirect('booking_confirmation', booking.id)
    else:
        form = BookingForm()
    return render(request, 'parking/payment.html', {'form': form, 'parking_space': parking_space})

@login_required
def booking_confirmation(request, id):
    booking = get_object_or_404(Booking, id=id)
    return render(request, 'parking/bookingconfirmation.html', {'booking': booking})
