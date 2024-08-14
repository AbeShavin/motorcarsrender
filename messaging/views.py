from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MessageForm
from members.models import Profile
from .models import Conversation


@login_required
def conversation_list(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    conversations = Conversation.objects.filter(participants=request.user)

    # Prepare data for each conversation
    conversation_data = []
    for conversation in conversations:
        partner = conversation.participants.exclude(id=request.user.id).first()
        last_message = conversation.messages.last()
        
        # Count unread messages from other participants
        unread_count = conversation.messages.filter(
            sender__in=conversation.participants.exclude(id=request.user.id),
            is_read=False
        ).count()
        
        conversation_data.append({
            'conversation': conversation,
            'partner': partner,
            'last_message': last_message,
            'unread_count': unread_count,
        })

    return render(request, 'messaging/conversation_list.html', {'conversation_data': conversation_data, 'profile': user_profile})


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in conversation.participants.all():
        return redirect('conversation_list')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            # Mark all messages in this conversation as read for this user
            conversation.messages.filter(
                sender__in=conversation.participants.exclude(id=request.user.id),
                is_read=False
            ).update(is_read=True)
            return redirect('conversation_detail', pk=conversation.pk)
    else:
        form = MessageForm()

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'form': form
    })

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    if other_user == request.user:
        return redirect('conversation_list')
      
    # Check if a conversation already exists
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)
        conversation.participants.add(other_user)
     
    return redirect('conversation_detail', pk=conversation.pk)

@login_required
def delete_conversation(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)

    if request.method == 'POST':
        conversation.delete()
        return redirect('conversation_list')

    return render(request, 'messaging/delete_conversation.html', {'conversation': conversation})
