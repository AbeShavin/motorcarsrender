from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from car_listing.models import Car, Favorite
from car_listing.forms import CarSearchForm
from messaging.models import Conversation
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def home(request):
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
    return render(request, 'home.html', {'form': form, 'cars': cars})
  
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    user_cars = Car.objects.filter(owner=user)
    car_count = user_cars.count()
    return render(request, 'profile.html', {
        'profile': profile,
        'user_cars': user_cars,
        'car_count': car_count,
        'profile_user': user  # pass the user object to the template
    })

@login_required
def member_conversations(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('members')  # Redirect to refresh the page and hide the form
    else:
        form = ProfileForm(instance=user_profile)
    
    user_cars = Car.objects.filter(owner=request.user)
    car_count = user_cars.count()
    
    conversations = Conversation.objects.filter(participants=request.user)
    conversation_data = []
    for conversation in conversations:
        partner = conversation.participants.exclude(id=request.user.id).first()
        last_message = conversation.messages.last()
        conversation_data.append({
            'conversation': conversation,
            'partner': partner,
            'last_message': last_message,
        })
 
    return render(request, 'member_conversations.html', {
        'user_cars': user_cars,
        'car_count': car_count,
        'conversation_data': conversation_data,
        'profile': user_profile,
        'profile_form': form,
        'profile_complete': user_profile.is_complete()
    })  



@login_required
def members(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('members')  # Redirect to refresh the page and hide the form
    else:
        form = ProfileForm(instance=user_profile)
    favorites = Favorite.objects.filter(user=request.user)
    user_cars = Car.objects.filter(owner=request.user)
    car_count = user_cars.count()
    
    conversations = Conversation.objects.filter(participants=request.user)
    conversation_data = []
    for conversation in conversations:
        partner = conversation.participants.exclude(id=request.user.id).first()
        last_message = conversation.messages.last()
        conversation_data.append({
            'conversation': conversation,
            'partner': partner,
            'last_message': last_message,
        }) 

    return render(request, 'memberhome.html', {
        'favorites': favorites,
        'user_cars': user_cars,
        'car_count': car_count,
        'conversation_data': conversation_data,
        'profile': user_profile,
        'profile_form': form,
        'profile_complete': user_profile.is_complete()
    })   
