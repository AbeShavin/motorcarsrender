from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from car_listing.models import Car, Favorite
from messaging.models import Conversation
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')
  
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
