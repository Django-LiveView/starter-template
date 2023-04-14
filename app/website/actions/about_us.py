from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    get_html,
    update_active_nav,
    enable_lang,
    loading,
)
from core import settings
from random import randint

template = "pages/about_us.html"


async def get_context(consumer=None):
    context = get_global_context(consumer=consumer)
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("about us"),
            "title": _("About us") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("About us page of the website"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "about us",
            "page": template,
        }
    )
    return context


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    # Nav
    await update_active_nav(consumer, "about us")
    # Main
    my_context = await get_context(consumer=consumer)
    html = await get_html(template, my_context)
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": html,
    }
    data.update(my_context)
    await consumer.send_html(data)


async def update_random_number_text(consumer, client_data):
    """Update random number with plain text"""
    data = {
        "action": client_data["action"],
        "selector": "#content-random-number-text",
        "html": str(randint(0, 100)),
    }
    await consumer.send_html(data)


async def update_random_number_html(consumer, client_data):
    """Update random number with HTML"""
    html = await get_html("components/_random_number.html", {"number": randint(0, 100)})
    data = {
        "action": client_data["action"],
        "selector": "#content-random-number-html",
        "html": html,
    }
    await consumer.send_html(data)
