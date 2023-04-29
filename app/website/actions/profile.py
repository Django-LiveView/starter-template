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
    get_image_from_base64,
)
from core import settings


template = "pages/profile.html"

# Database


@database_sync_to_async
def save_avatar(user, filename, file_data):
    user.profile.avatar.save(filename, file_data)


# Functions


async def get_context(consumer=None, lang=None):
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


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    # Nav
    await update_active_nav(consumer, "profile")
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


@loading
async def update_avatar(consumer, client_data):
    if "mimeType" in client_data["data"] and client_data["data"]["mimeType"] in (
        "image/jpeg",
        "image/png",
        "image/webp",
    ):
        # Variables
        user = consumer.scope["user"]
        my_file, my_filename = get_image_from_base64(
            client_data["data"]["base64"], client_data["data"]["mimeType"]
        )
        # Update avatar
        user = consumer.scope["user"]
        await save_avatar(user, my_filename, my_file)
        # Update HTML
        html = await get_html("components/_avatar.html", {"user": user})
        data = {
            "action": "update_avatar",
            "selector": "#avatar__container",
            "html": html,
        }
        await consumer.send_html(data)
    else:
        # Bad extension image. Send message
        await send_notification(consumer, _("Bad extension image"), "danger")
