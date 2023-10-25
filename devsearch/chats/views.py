from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Max
from django.db import models

from .utils import insert_line_breaks
from .models import Message, Room
from users.models import Profile



# @login_required(login_url="login")
# def inbox(request):
#     profile = request.user.profile
#     received_messages = Message.objects.filter(chat_room__icontains=profile.username)
#     unread_message_count = Message.objects.filter(recipient=request.user.profile, is_read=False).count()

#     context = {
#         "unread_message_count": unread_message_count,
#         "received_messages": received_messages
#     }

#     return render(request, "chats/inbox.html", context)



@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    rooms = Room.objects.filter(members=profile)

    for room in rooms:
        room.partner = room.get_partner(profile)

    return render(request, 'chats/inbox.html', {'rooms': rooms})



@login_required(login_url="login")
def private_chat_view(request, pk):
    profile = request.user.profile
    room = Room.objects.get(id=pk)
    other_user_profile = room.get_partner(profile)
    chat_messages = room.messages.all().reverse()
    
    for chat_message in chat_messages:
        chat_message.content = insert_line_breaks(chat_message.content)

    return render(request, 'chats/room.html', {
        'chat_messages': chat_messages,
        'room': room,
        'profile': profile,
        'other_user': other_user_profile
    })