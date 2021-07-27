"""
ASGI config for hospital project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
#https://channels.readthedocs.io/en/stable/topics/routing.html#protocoltyperouter
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from appointment.consumers import TestConsumer
application = get_asgi_application()
#s_patterns =[
#   path('test/',TestConsumer)
#

from .routing import ws_application
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter(ws_application)
    )
    )
})
