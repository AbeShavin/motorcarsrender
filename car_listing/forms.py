from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from django import forms
from .models import Car, CarImage, CarMake, CarModel, Favorite
from .widgets import MultipleFileInput
from django import forms


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = []  # No fields needed for adding favorites

class CarImageDeleteForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = []  # no fields needed for deletion


class CarForm(forms.ModelForm):
    make = forms.ModelChoiceField(queryset=CarMake.objects.all(), required=True)
    model = forms.ModelChoiceField(queryset=CarModel.objects.none(), required=True)

    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'price', 'mileage', 'description', 'zipcode', 'vin', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'make' in self.data:
            try:
                make_id = int(self.data.get('make'))
                self.fields['model'].queryset = CarModel.objects.filter(make_id=make_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['model'].queryset = CarModel.objects.none()
        elif self.instance.pk:
            self.fields['model'].queryset = self.instance.make.carmodel_set.order_by('name')
   
class CarImageForm(forms.ModelForm):
    image = forms.ImageField(widget=MultipleFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = CarImage
        fields = ['image']


class CarSearchForm(forms.Form):
    year_min = forms.IntegerField(
        required=False, 
        initial=2000, 
        max_value=2026, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )
    year_max = forms.IntegerField(
        required=False, 
        initial=2025, 
        max_value=2026, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )
    make = forms.ModelChoiceField(
        queryset=CarMake.objects.all(), 
        required=False, 
        empty_label="All Makes",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': ' '})
    )
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.none(), 
        required=False, 
        empty_label="All Models",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': ' '})
    )
    price_min = forms.DecimalField(
        required=False, 
        initial=None, 
        min_value=0, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )
    price_max = forms.DecimalField(
        required=False, 
        initial=None, 
        min_value=0, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )
    mileage_min = forms.IntegerField(
        required=False, 
        initial=0, 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )
    mileage_max = forms.IntegerField(
        required=False, 
        initial=200000, 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )
    zipcode = forms.CharField(
        required=False, 
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )
    radius = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'make' in self.data:
            try:
                make_id = int(self.data.get('make'))
                self.fields['model'].queryset = CarModel.objects.filter(make_id=make_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['model'].queryset = CarModel.objects.none()
        elif 'model' in self.data:
            self.fields['model'].queryset = CarModel.objects.none()


class ggCarSearchForm(forms.Form):
    year_min = forms.IntegerField(required=False, initial=1990, max_value=2026) 
    year_max = forms.IntegerField(required=False, initial=2024, max_value=2026) 
    make = forms.ModelChoiceField(queryset=CarMake.objects.all(), required=False, empty_label="Select Make")
    model = forms.ModelChoiceField(queryset=CarModel.objects.none(), required=False, empty_label="Select Model")
    price_min = forms.DecimalField(required=False, initial=0, min_value=0, decimal_places=2)
    price_max = forms.DecimalField(required=False, initial=20000, min_value=0, decimal_places=2)
    mileage_min = forms.IntegerField(required=False, initial=0, min_value=0) 
    mileage_max = forms.IntegerField(required=False, initial=100000, min_value=0) 
    zipcode = forms.CharField(required=False, max_length=10)
    radius = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'make' in self.data:
            try:
                make_id = int(self.data.get('make'))
                self.fields['model'].queryset = CarModel.objects.filter(make_id=make_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['model'].queryset = CarModel.objects.none()
        elif 'model' in self.data:
            self.fields['model'].queryset = CarModel.objects.none()
    