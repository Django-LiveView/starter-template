from core import settings
from channels.db import database_sync_to_async
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    get_html,
    update_active_nav,
    send_notification,
    enable_lang,
    loading,
    get_image_from_base64,
)
from app.website.forms import CatForm
from app.website.actions import cats
from django.core.files.uploadedfile import SimpleUploadedFile


template = "pages/new_cat.html"

# Database


# Functions


async def get_context(consumer=None, form=None):
    context = get_global_context(consumer=consumer)
    # Check client_data["data"]["form"] exist
    if not form:
        form = CatForm()
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("cat new"),
            "title": _("New cat") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("New cat page of the website"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "",
            "page": template,
            "form": form,
        }
    )
    return context


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    # Nav
    await update_active_nav(consumer, "")
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


@enable_lang
@loading
async def create(consumer, client_data, lang=None):
    if client_data and "data" in client_data and "form" in client_data["data"]:
        # Add file to input image
        base64_str = client_data["data"]["form"]["avatar"]["base64"]
        mime_type = client_data["data"]["form"]["avatar"]["mimeType"]
        # Create byte file from base64
        my_file_bytes, my_filename = get_image_from_base64(
            base64_str, mime_type, is_file=False
        )
        # Set data in form
        form = CatForm(
            client_data["data"]["form"],
            {
                "avatar": SimpleUploadedFile(
                    my_filename,
                    my_file_bytes,
                    content_type=mime_type,
                )
            },
        )
        if form.is_valid():
            # Create cat
            await form.save()
            # Send notification
            await send_notification(consumer, _("A cat is born!"), "success")
            # Redirect to cats list
            await cats.send_page(consumer, client_data, lang=lang)
        else:
            # Send form errors
            my_context = await get_context(consumer=consumer)
            my_context.update({"form": form})
            html = await get_html(template, my_context)
            data = {
                "action": client_data["action"],
                "selector": "#main",
                "html": html,
            }
            data.update(my_context)
            await consumer.send_html(data)
