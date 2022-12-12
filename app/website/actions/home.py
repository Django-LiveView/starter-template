
from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _, get_language
from app.website.actions.utils import (
    toggle_loading,
    update_active_nav,
)
from core import settings


template = "pages/home.html"


def get_context():
    context = get_global_context()
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("home"),
            "title": "",
            "meta": {
                "description": _(
                    "Home page of the website"
                ),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "page": template,
        }
    )
    return context


def get_html():
    return render_to_string(template, get_context())


def send_page(consumer, client_data):
    # Show loading
    toggle_loading(consumer, True)
    # Nav
    update_active_nav(consumer, "home")
    # Main
    data = {"action": client_data["action"], "selector": "#main", "html": get_html()}
    data.update(get_context())
    consumer.send_html(data)
    # Hide loading
    toggle_loading(consumer, False)
