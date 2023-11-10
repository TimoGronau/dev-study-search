from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Max
from django.db import models

from .models import Message, Room
from users.models import Profile



@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    rooms = Room.objects.filter(members=profile)
    unread_message_count = Message.objects.filter(recipient=request.user.profile, is_read=False).count()


    for room in rooms:
        room.partner = room.get_partner(profile)

    context = {
        "rooms": rooms,
        "unread_message_count": unread_message_count,
    }

    return render(request, 'chats/inbox.html', context)



@login_required(login_url="login")
def private_chat_view(request, pk):
    profile = request.user.profile
    room = Room.objects.get(id=pk)
    other_user_profile = room.get_partner(profile)
    chat_messages = room.messages.all().reverse()

    for cm in chat_messages:
        if cm.sender != profile:
            cm.is_read = True
            cm.save()
    
    return render(request, 'chats/room.html', {
        'chat_messages': chat_messages,
        'room': room,
        'profile': profile,
        'other_user': other_user_profile
    })

    