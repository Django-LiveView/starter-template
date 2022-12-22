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


template = "pages/profile.html"


def get_context(consumer=None, lang=None):
    context = get_global_context(consumer=consumer)
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("profile"),
            "title": _("Profile") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("Profile"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "profile",
            "page": template,
        }
    )
    return context


def get_html(consumer=None, lang=None):
    return render_to_string(template, get_context(consumer=consumer, lang=lang))


@enable_lang
@loading
def send_page(consumer, client_data, lang=None):
    # Nav
    update_active_nav(consumer, "profile")
    # Main
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": get_html(consumer, lang=lang),
    }
    data.update(get_context(consumer=consumer, lang=lang))
    consumer.send_html(data)
