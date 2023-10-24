
from django.urls import path , include
from chats.consumers import ChatConsumer
 

websocket_urlpatterns = [
    path('ws/<str:roomId>/', ChatConsumer.as_asgi()),
]