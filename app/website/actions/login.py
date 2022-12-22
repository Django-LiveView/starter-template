from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    update_active_nav,
    enable_lang,
    loading,
)
from core import settings
from app.website.forms import LoginForm
from app.website.models import User, Client
from django.contrib.auth import authenticate
from channels.auth import login, logout
from asgiref.sync import async_to_sync
from app.website.actions import home
from app.website.actions import profile


template = "pages/login.html"


def get_context(consumer=None, lang=None):
    context = get_global_context(consumer=consumer)
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("login"),
            "title": _("Login") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("Login"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "login",
            "page": template,
            "form": LoginForm(),
            "users": User.objects.filter(is_staff=False),
        }
    )
    return context


def get_html(consumer=None, lang=None):
    return render_to_string(template, get_context(consumer=consumer, lang=lang))


@enable_lang
@loading
def send_page(consumer, client_data, lang=None):
    # Nav
    update_active_nav(consumer, "login")
    # Main
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": get_html(lang=lang),
    }
    data.update(get_context(consumer=consumer, lang=lang))
    consumer.send_html(data)


@enable_lang
@loading
def log_in(consumer, client_data, lang=None):
    """Log in user"""
    form = LoginForm(client_data["data"])
    # Check if form is valid
    if form.is_valid():
        auth = authenticate(
            username=form.cleaned_data["email"].strip(),
            password=form.cleaned_data["password"].strip(),
        )
        if auth:
            # Log in
            async_to_sync(login)(consumer.scope, auth)
            consumer.scope["session"].save()
            # Save user association with client
            Client.objects.filter(user=auth).delete()
            Client.objects.filter(channel_name=consumer.channel_name).update(user=auth)
            # Redirect to profile
            profile.send_page(consumer, client_data, lang=lang)
        else:
            # Info to user that email or password is incorrect
            form.add_error("email", _("Invalid email or password"))
            data = {
                "action": client_data["action"],
                "selector": "#login__form",
                "html": render_to_string("forms/login.html", {"form": form}),
            }
            consumer.send_html(data)
    else:
        # Send errors
        data = {
            "action": client_data["action"],
            "selector": "#login__form",
            "html": render_to_string("forms/login.html", {"form": form}),
        }
        consumer.send_html(data)

        
@enable_lang
@loading
def log_out(consumer, client_data, lang=None):
    """Log out user"""
    async_to_sync(logout)(consumer.scope)
    consumer.scope["session"].save()
    # Redirect to home
    home.send_page(consumer, client_data, lang=lang)
