"""
ASGI config for homecourt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import drills.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homecourt.settings')

application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application(),
        "websocket" : AuthMiddlewareStack(
                URLRouter(drills.routing.websocket_urlpatterns)
            )
        
    }
)
