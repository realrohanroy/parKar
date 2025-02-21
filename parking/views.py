from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ParkingSpace, Booking, ParkingSpacePhoto
from .forms import BookingForm, RegisterForm, LoginForm, ParkingSpaceForm
from django.contrib.auth import login, authenticate, logout

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

@login_required(login_url='authentications')
def listingpage(request):
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST)
        if form.is_valid():
            # Store the form data in the session
            request.session['parking_space_data'] = form.cleaned_data
            return redirect('addphotos')  # Redirect to add photos
    else:
        form = ParkingSpaceForm()
    return render(request, 'parking/listingpage.html', {'form': form})

@login_required
def add_photos(request):
    if request.method == 'POST':
        images = request.FILES.getlist('image')
        
        if len(images) < 3:
            return render(request, 'parking/addphotos.html', {'error': 'Please upload at least 3 photos'})
        
        # Create the parking space object from session data
        parking_space_data = request.session.get('parking_space_data')
        if parking_space_data:
            parking_space = ParkingSpace(**parking_space_data)
            parking_space.user = request.user  # Set the user
            parking_space.save()  # Save the parking space to the database
            
            # Save uploaded photos
            for img in images[:10]:
                ParkingSpacePhoto.objects.create(parking_space=parking_space, image=img)
            
            # Clear the session data
            del request.session['parking_space_data']
            
            return redirect('parking/setpricing', space_id=parking_space.id)  # Redirect to set pricing
    return render(request, 'parking/addphotos.html')

@login_required
def set_pricing(request, space_id):
    parking_space = get_object_or_404(ParkingSpace, id=space_id, user=request.user)
    
    if request.method == 'POST':
        # Assuming you have a form to set pricing
        pricing = request.POST.get('pricing')  # Get pricing from the form
        parking_space.price_per_hour = pricing  # Set the pricing
        parking_space.save()  # Save the updated parking space
        
        return redirect('home')  # Redirect to home or another page after setting pricing
    
    return render(request, 'parking/setpricing.html', {'parking_space': parking_space})

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

# views.py
from django.shortcuts import render

def dummy_page(request):
    return render(request, 'parking/dummypage.html')
def dummy_page2(request):
    return render(request, 'parking/dummypage2.html')
def dummy_page3(request):
    return render(request, 'parking/dummypage3.html')
def dummy_page4(request):
    return render(request, 'parking/dummypage4.html')

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