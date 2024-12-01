"""
ASGI config for the project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import src.modules.tools.routing
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(src.modules.tools.routing.websocket_urlpatterns))
        ),
        # "websocket": URLRouter(src.modules.tools.routing.websocket_urlpatterns),
    }
)
