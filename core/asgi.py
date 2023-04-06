import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from app.website.consumers import WebsiteConsumer


application = ProtocolTypeRouter(
    {
        # Django's ASGI application to handle traditional HTTP requests
        "http": get_asgi_application(),
        # WebSocket handler
        "websocket": AuthMiddlewareStack(
            AllowedHostsOriginValidator(
                URLRouter([re_path(r"^ws/website/$", WebsiteConsumer.as_asgi())])
            )
        ),
    }
)
