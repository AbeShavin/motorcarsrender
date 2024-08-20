from django.db import models
from django.contrib.auth.models import User

class VehicleProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_profiles')
    vehicle_type = models.CharField(max_length=100)
    year = models.IntegerField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    mileage = models.IntegerField()
    zipcode = models.CharField(max_length=10)
    email = models.EmailField()
    engine_modifications = models.TextField(blank=True, null=True)
    transmission_modifications = models.TextField(blank=True, null=True)
    body_modifications = models.TextField(blank=True, null=True)
    brake_modifications = models.TextField(blank=True, null=True)
    suspension_modifications = models.TextField(blank=True, null=True)
    rims_tires = models.TextField(blank=True, null=True)
    mechanic_builder = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.owner.username}"

class VehicleImage(models.Model):
    vehicle_profile = models.ForeignKey(VehicleProfile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.vehicle_profile.make} {self.vehicle_profile.model}"

class Comment(models.Model):
    vehicle_profile = models.ForeignKey(VehicleProfile, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.vehicle_profile.make} {self.vehicle_profile.model}"
