from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'contact_number', 'zipcode', 'seller_type', 'image']
        widgets = {
            'seller_type': forms.RadioSelect,  # Provides radio buttons for user type selection
        }