from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, CarImage, CarModel, Favorite
from .forms import CarForm, CarSearchForm,CarImageForm
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Q
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
    
def load_models(request):
    make_id = request.GET.get('make')
    models = CarModel.objects.filter(make_id=make_id).values('id', 'name')
    return JsonResponse(list(models), safe=False)


def notify_car_owner(car):
    owner_email = car.owner.email  # Assuming `owner` is a ForeignKey to User in the Car model
    send_mail(
        'Your Car Has a New Favorite!',
        f'Your car {car.make} {car.model} has been favorited.',
        settings.DEFAULT_FROM_EMAIL,
        [owner_email],
        fail_silently=False,
    )


POSTING_LIMIT = 5

def car_search(request):
    form = CarSearchForm(request.GET or None)
    return render(request, 'car_listing/car_search.html', {'form': form})



def search_results(request):
    form = CarSearchForm(request.GET or None)
    cars = Car.objects.all()

    if form.is_valid():
        make_id = form.cleaned_data.get('make')
        model_id = form.cleaned_data.get('model')
        year_min = form.cleaned_data.get('year_min')
        year_max = form.cleaned_data.get('year_max')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        mileage_min = form.cleaned_data.get('mileage_min')
        mileage_max = form.cleaned_data.get('mileage_max')
        zipcode = form.cleaned_data.get('zipcode')
        radius = form.cleaned_data.get('radius')

        
        if make_id:
            cars = cars.filter(make_id=make_id)
        if model_id:
            cars = cars.filter(model_id=model_id)
        if year_min:
            cars = cars.filter(year__gte=year_min)
        if year_max:
            cars = cars.filter(year__lte=year_max)
        if price_min:
            cars = cars.filter(price__gte=price_min)
        if price_max:
            cars = cars.filter(price__lte=price_max)
        if mileage_min:
            cars = cars.filter(mileage__gte=mileage_min)
        if mileage_max:
            cars = cars.filter(mileage__lte=mileage_max)
                # Handle location-based filtering
        if zipcode and radius:  # Ensure both are provided
            geolocator = Nominatim(user_agent="car_listing", timeout=10)
            try:
                location = geolocator.geocode(zipcode, country_codes="US")
                if location:
                    user_lat = location.latitude
                    user_lon = location.longitude

                    # Filter by distance
                    filtered_listings = []
                    for car in cars:
                        if car.latitude and car.longitude:
                            car_location = (car.latitude, car.longitude)
                            user_location = (user_lat, user_lon)
                            distance = geodesic(car_location, user_location).miles
                            if distance <= radius:
                                filtered_listings.append(car)
                    cars = filtered_listings
                else:
                    form.add_error('zipcode', 'Invalid zip code.')
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                form.add_error('zipcode', f'Geocoding service error: {e}')
        elif zipcode:
            form.add_error('radius', 'Radius is required for zip code search.')

    paginator = Paginator(cars, 20)  # cars per page
    page = request.GET.get('page')
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)

    return render(request, 'car_listing/search_results.html', {'form': form, 'cars': cars})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    is_favorited = Favorite.objects.filter(user=request.user, car=car).exists() if request.user.is_authenticated else False
    return render(request, 'car_listing/car_detail.html', {'car': car, 'is_favorited': is_favorited})

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


@login_required
def add_favorite(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, car=car)
    notify_car_owner(car)
    return redirect('car_detail', pk=car_id)

@login_required
def remove_favorite(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    Favorite.objects.filter(user=request.user, car=car).delete()
    return redirect('car_detail', pk=car_id)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'car_listing/favorite_list.html', {'favorites': favorites})
