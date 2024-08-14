
from django.db import models
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from .validators import validate_vin

class CarMake(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
class Car(models.Model):
        
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    zipcode = models.PositiveIntegerField()
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='car_images/')
    vin = models.CharField(max_length=17, unique=True, null=True, blank=True, validators=[validate_vin])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.zipcode:
            geolocator = Nominatim(user_agent="car_listing")
            try:
                location = geolocator.geocode(self.zipcode, country_codes="US")
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                print(f"Geocoding service error: {e}")

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.make} {self.model} ({self.year})'
    
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='car_images/')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} - {self.car.make} {self.car.model}"

