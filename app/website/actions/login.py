from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.actions.utils import (
    update_active_nav,
    enable_lang,
    loading,
)
from core import settings
from app.website.forms import LoginForm


template = "pages/login.html"


def get_context(lang=None):
    context = get_global_context()
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("login"),
            "title": _("login") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("Login"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "login",
            "page": template,
            "form": LoginForm(),
        }
    )
    return context


def get_html(lang=None):
    return render_to_string(template, get_context(lang=lang))


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
    data.update(get_context(lang=lang))
    consumer.send_html(data)
