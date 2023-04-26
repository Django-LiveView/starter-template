from core import settings
from channels.db import database_sync_to_async
from django.templatetags.static import static
from app.website.models import Cat
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    get_html,
    update_active_nav,
    enable_lang,
    loading,
)


template = "pages/home.html"

# Database


@database_sync_to_async
def get_first_cat():
    return Cat.objects.first()


# Functions


async def get_context(consumer=None):
    context = get_global_context(consumer=consumer)
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("home"),
            "title": _("Home") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("Home page of the website"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "home",
            "page": template,
            "first_cat": await get_first_cat(),
        }
    )
    return context


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    # Nav
    await update_active_nav(consumer, "home")
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
