
from django.db import models
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class Car(models.Model):
    MAKE_CHOICES = [
        ('Acura', 'Acura'),
        ('Alfa Romeo', 'Alfa Romeo'),
        ('Aston Martin', 'Aston Martin'),
        ('Audi', 'Audi'),
        ('Bentley', 'Bentley'),
        ('BMW', 'BMW'),
        ('Buick', 'Buick'),
        ('Cadillac', 'Cadillac'),
        ('Chevrolet', 'Chevrolet'),
        ('Chrysler', 'Chrysler'),
        ('Dodge', 'Dodge'),
        ('Datsun', 'Datsun'),
        ('Eagle', 'Eagle'),
        ('Ferrari', 'Ferrari'),
        ('Fiat', 'Fiat'),
        ('Ford', 'Ford'),
        ('Genesis', 'Genesis'),
        ('GMC', 'GMC'),
        ('Honda', 'Honda'),
        ('Hyundai', 'Hyundai'),
        ('Infiniti', 'Infinity'),
        ('Isuzu', 'Isuzu'),
        ('Jaguar', 'Jaguar'),
        ('Jeep', 'Jeep'),
        ('Kia', 'Kia'),
        ('Lamborghini', 'Lamborghini'),
        ('Land Rover', 'Land Rover'),
        ('Lexus', 'Lexus'),
        ('Lincoln', 'Lincoln'),
        ('Maserati', 'Maserati'),
        ('Mazda', 'Mazda'),
        ('McLaren', 'McLaren'),
        ('Mercedes Benz', 'Mercedes Benz'),
        ('Mini', 'Mini'),
        ('Mitsubishi', 'Mitsubishi'),
        ('Nissan', 'Nissan'),
        ('Oldsmobile', 'Oldsmobile'),
        ('Pagani', 'Pagani'),
        ('Pontiac', 'Pontiac'),
        ('Porsche', 'Porsche'),
        ('RAM', 'RAM'),
        ('Rolls Royce', 'Rolls Royce'),
        ('Saab', 'Saab'),
        ('Subaru', 'Subaru'),
        ('Tesla', 'Tesla'),
        ('Toyota', 'Toyota'),
        ('Volkswagen', 'Volkswagen'),
        ('Volvo', 'Volvo')
        
        # Add other makes as needed
    ]

    MODEL_CHOICES = [
        ('Acura', 'Integra'),
        ('Acura', 'RSX'),
        ('Audi', 'A4'),
        ('Audi', 'A6'),
        ('Audi', 'A8'),
        ('BMW', '1 Series'),
        ('BMW', '3 Series'),
        ('BMW', '5 Series'),
        ('BMW', 'M3'),
        ('BMW', 'M5'),
        ('Toyota', 'Camry'),
        ('Corolla', 'Corolla'),
        ('A4', 'A4'),
        ('Grand National', 'Grand National'),
        ('Civic', 'Civic'),
        ('Q45', 'Q45'),
        ('911 Turbo', '911 Turbo'),
        ('F-150', 'F-150'),
        ('Silverado', 'Silverdao'),
        # Add other models as needed
    ]

    TYPE_CHOICES = [
        ('EV', 'EV'),
        ('Sedan', 'Sedan'),
        ('Sportscar', 'Sportscar'),
        ('Supercar','Supercar'),
        ('Truck/4x4/Offroad', 'Truck/4x4/Offroad'),
        ('Race/Drift/Modified', 'Race/Drift/Modified')  
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True)
    make = models.CharField(max_length=50, choices=MAKE_CHOICES)
    model = models.CharField(max_length=50, choices=MODEL_CHOICES)
    year = models.PositiveIntegerField()
    zipcode = models.CharField(max_length=10,default='33021')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='car_images/')
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