from django.db import models
from django.contrib.auth.models import User

class ParkingSpace(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    security_features = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=10, unique=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.parking_space.name}"

