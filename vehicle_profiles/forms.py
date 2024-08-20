from django import forms
from .models import VehicleProfile, VehicleImage, Comment

class VehicleProfileForm(forms.ModelForm):
    class Meta:
        model = VehicleProfile
        fields = [
            'vehicle_type', 'year', 'make', 'model', 'mileage', 'zipcode', 'email',
            'engine_modifications', 'transmission_modifications', 'body_modifications',
            'brake_modifications', 'suspension_modifications', 'rims_tires', 
            'mechanic_builder', 'description'
        ]

class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
