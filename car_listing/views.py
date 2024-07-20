# car_listing/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, CarImage
from .forms import CarForm, CarSearchForm,CarImageForm
from django.http import HttpResponseForbidden
from django.db.models import Q
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

POSTING_LIMIT = 5

def car_search(request):
    form = CarSearchForm(request.GET or None)
    cars = Car.objects.all()

    if form.is_valid():
        category = form.cleaned_data.get('category')
        make = form.cleaned_data.get('make')
        model = form.cleaned_data.get('model')
        year_min = form.cleaned_data.get('year_min')
        year_max = form.cleaned_data.get('year_max')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        zipcode = form.cleaned_data.get('zipcode')
        radius = form.cleaned_data.get('radius')

        if category:
            cars = cars.filter(make__icontains=category)
        if make:
            cars = cars.filter(make__icontains=make)
        if model:
            cars = cars.filter(model__icontains=model)
        if year_min:
            cars = cars.filter(year__gte=year_min)
        if year_max:
            cars = cars.filter(year__lte=year_max)
        if price_min:
            cars = cars.filter(price__gte=price_min)
        if price_max:
            cars = cars.filter(price__lte=price_max)

        if zipcode:
            geolocator = Nominatim(user_agent="car_listing", timeout=10)  # Set timeout to 10 seconds
            try:
                location = geolocator.geocode(zipcode, country_codes="US")
                if location and radius:
                    user_lat = location.latitude
                    user_lon = location.longitude

                    # Filter by distance
                    filtered_listings = []
                    for car in cars:
                        if car.latitude and car.longitude:
                            listing_location = (car.latitude, car.longitude)
                            user_location = (user_lat, user_lon)
                            distance = geodesic(listing_location, user_location).miles
                            if distance <= radius:
                                filtered_listings.append(car)

                    cars = filtered_listings
                else:
                    # Handle invalid zip code or radius
                    cars = []
                    form.add_error('zipcode', 'Invalid zip code or radius.')
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                # Handle geocoding service errors
                cars = []
                form.add_error('zipcode', f'Geocoding service error: {e}')
        else:
            form.add_error('zipcode', 'Zip code is required for radius search.')

    return render(request, 'car_listing/car_search.html', {'form': form, 'cars': cars})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'car_listing/car_detail.html', {'car': car})

@login_required
def car_create(request):
    if Car.objects.filter(owner=request.user).count() >= POSTING_LIMIT:
        return render(request, 'car_listing/posting_limit_reached.html', {'POSTING_LIMIT': POSTING_LIMIT})
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        image_form = CarImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            for f in files:
                CarImage.objects.create(car=car, image=f)
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm()
        image_form = CarImageForm()
    return render(request, 'car_listing/car_form.html', {'form': form,'image_form': image_form,})

@login_required
def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)
    
    if car.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit this listing.")
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        files = request.FILES.getlist('image')
        if form.is_valid():
            form.save()
            for f in files:
                CarImage.objects.create(car=car, image=f)
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm(instance=car)
        image_form = CarImageForm()
    return render(request, 'car_listing/car_form.html', {'form': form,'image_form': image_form,})

@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if car.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this listing.")
    if request.method == 'POST':
        car.delete()
        return redirect('account_login')
    return render(request, 'car_listing/car_confirm_delete.html', {'car': car})

