from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from car_listing.models import Car
from messaging.models import Conversation

def home(request):
    return render(request, 'home.html')

@login_required
def members(request):
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

    return render(request, 'memberhome.html', {'user_cars': user_cars, 'car_count': car_count, 'conversation_data': conversation_data})
