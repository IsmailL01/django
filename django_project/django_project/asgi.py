"""
ASGI config for django_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from  channels.routing import get_default_application, ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddleware
from  snake.routing import websocket_urlpatterns

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()
application = get_default_application()


application = ProtocolTypeRouter({
    'http': get_default_application(),
    "websocket": AuthMiddleware({
        URLRouter(websocket_urlpatterns)
    })
})

