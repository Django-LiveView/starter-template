# ccstech/asgi.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ccstech.settings")
django.setup()

from django.conf import settings
from django.core.asgi import get_asgi_application
from channels.security.websocket import OriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from app.website.consumers import WebsiteConsumer
import os
from django.core.asgi import get_asgi_application
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asgi_example.settings")

# Observability
import json
from re import search
from datetime import datetime


def server_request_hook(span, scope):
    if span and span.is_recording():
        today = datetime.now()
        span.set_attribute("create_at", today.isoformat())
        response = dict(scope)
        if response and isinstance(response, object):
            headers = response.get("headers")
            asgi = response.get("asgi")
            if headers:
                span.set_attribute("headers", str(headers))
            if asgi:
                span.set_attribute("asgi.version", asgi.get("version"))
            else:
                span.set_attribute("scope", str(scope))


def client_request_hook(span, scope):
    if span and span.is_recording():
        today = datetime.now()
        span.set_attribute("create_at", today.isoformat())
        response = dict(scope)
        if response and isinstance(response, object):
            headers = response.get("headers")
            client = response.get("client")
            server = response.get("server")
            asgi = response.get("asgi")
            if headers:
                span.set_attribute("headers", str(headers))
            if client:
                span.set_attribute("client.ip", client[0])
                span.set_attribute("client.port", client[1])
            if server:
                span.set_attribute("server.ip", server[0])
                span.set_attribute("server.port", server[1])
            if asgi:
                span.set_attribute("asgi.version", asgi.get("version"))
            else:
                span.set_attribute("scope", str(scope))


def client_response_hook(span, message):
    if span and span.is_recording():
        today = datetime.now()
        span.set_attribute("create_at", today.isoformat())
        response = dict(message)
        if response and isinstance(response, object):
            text_data = response.get("text")
            body = response.get("body")
            if text_data and search("{", text_data) and search("}", text_data):
                object_data = json.loads(text_data)
                if isinstance(object_data, object):
                    action = object_data.get("action")
                    selector = object_data.get("selector")
                    html = object_data.get("html")
                    append = object_data.get("append")
                    url = object_data.get("url")
                    span.set_attribute("action.action", action if action else "")
                    span.set_attribute("action.selector", selector if selector else "")
                    span.set_attribute("action.html", html if html else "")
                    span.set_attribute(
                        "action.append", append if len(str(append)) else ""
                    )
                    span.set_attribute("action.url", url if url else "")
            if body:
                span.set_attribute("html", body)


application = OpenTelemetryMiddleware(
    app=ProtocolTypeRouter(
        {
            # Django's ASGI application to handle traditional HTTP requests
            "http": get_asgi_application(),
            # WebSocket handler
            "websocket": OriginValidator(
                URLRouter([re_path(r"^ws/website/$", WebsiteConsumer.as_asgi())]),
                settings.ALLOWED_HOSTS,
            ),
        }
    ),
    server_request_hook=server_request_hook,
    client_request_hook=client_request_hook,
    client_response_hook=client_response_hook,
)
