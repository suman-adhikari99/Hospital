from django.urls import path
from channels.routing import URLRouter
from appointment.consumers import TestConsumer

ws_application= [
    path('ws/chat/',TestConsumer.as_asgi())
]