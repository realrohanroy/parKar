from django.db import models
from django.contrib.auth.models import User




from django.db import models

from django.db import models
from django.contrib.auth.models import User

class ParkingSpace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parking_spaces')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    security_features = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class ParkingSpacePhoto(models.Model):
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='parking_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo for {self.parking_space.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE, related_name='bookings')
    booking_id = models.CharField(max_length=10, unique=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.parking_space.name}"