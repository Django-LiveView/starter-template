from channels.db import database_sync_to_async
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    get_html,
    update_active_nav,
    enable_lang,
    loading,
    send_notification,
)
from core import settings
from app.website.forms import LoginForm
from app.website.models import User, Client
from django.contrib.auth import authenticate
from channels.auth import login, logout
from asgiref.sync import sync_to_async
from app.website.actions import home
from app.website.actions import profile


template = "pages/login.html"

# Database


@database_sync_to_async
def get_all_users():
    return list(User.objects.filter(is_staff=False).order_by("username"))

@database_sync_to_async
def save_client(auth, channel_name):
    Client.objects.filter(user=auth).delete()
    Client.objects.filter(channel_name=channel_name).update(user=auth)


# Functions


async def get_context(consumer=None, lang=None):
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
            "users": await get_all_users(),
        }
    )
    return context


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    # Nav
    await update_active_nav(consumer, "login")
    # Main
    my_context = await get_context(consumer=consumer, lang=lang)
    html = await get_html(template, my_context)
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": html,
    }
    data.update(my_context)
    await consumer.send_html(data)

@enable_lang
@loading
async def log_in(consumer, client_data, lang=None):
    """Log in user"""
    form = LoginForm(client_data["data"])
    # Check if form is valid
    if form.is_valid():
        auth = await sync_to_async(authenticate)(
            username=form.cleaned_data["email"].strip(),
            password=form.cleaned_data["password"].strip(),
        )
        if auth:
            # Log in
            await login(consumer.scope, auth)
            await database_sync_to_async(consumer.scope["session"].save)()
            # Save user association with client
            await save_client(auth, consumer.channel_name)
            # Redirect to profile
            await profile.send_page(consumer, client_data, lang=lang)
            # Send message
            await send_notification(consumer, _("You are now logged in!"), "success")
        else:
            # Info to user that email or password is incorrect
            form.add_error("email", _("Invalid email or password"))
            data = {
                "action": client_data["action"],
                "selector": "#login__form",
                "html": render_to_string("forms/login.html", {"form": form}),
            }
            await consumer.send_html(data)
    else:
        # Send errors
        data = {
            "action": client_data["action"],
            "selector": "#login__form",
            "html": render_to_string("forms/login.html", {"form": form}),
        }
        await consumer.send_html(data)


@enable_lang
@loading
async def log_out(consumer, client_data, lang=None):
    """Log out user"""
    await logout(consumer.scope)
    await database_sync_to_async(consumer.scope["session"].save)()
    # Redirect to home
    await home.send_page(consumer, client_data, lang=lang)
    # Send message
    await send_notification(consumer, _("You are now logged out!"), "success")
