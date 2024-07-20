from django import forms
from .models import Car, CarImage
from .widgets import MultipleFileInput

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['category', 'make', 'model', 'year', 'price', 'description', 'zipcode', 'image']

class CarImageForm(forms.ModelForm):
    image = forms.ImageField(widget=MultipleFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = CarImage
        fields = ['image']

class CarSearchForm(forms.Form):
    category = forms.ChoiceField(choices=[('', 'Any')] + Car.TYPE_CHOICES, required=False )
    year_min = forms.IntegerField(required=False, label='Year (min)')
    year_max = forms.IntegerField(required=False, label='Year (max)')
    make = forms.ChoiceField(choices=[('', 'Any')] + Car.MAKE_CHOICES, required=False)
    model = forms.ChoiceField(choices=[('', 'Any')] + Car.MODEL_CHOICES, required=False)
    price_min = forms.DecimalField(required=False, min_value=0, decimal_places=2)
    price_max = forms.DecimalField(required=False, min_value=0, decimal_places=2)
    zipcode = forms.CharField(required=False, max_length=5)
    radius = forms.FloatField()