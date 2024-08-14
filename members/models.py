from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('private', 'Private Seller'),
        ('dealer', 'Dealer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    seller_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def is_complete(self):
        # Return True if profile is considered complete
        return all([
            self.address,
            self.contact_number,
            self.zipcode,
            self.seller_type,
            self.image,
        ])
