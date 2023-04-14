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
    send_email,
    send_notification,
)
from core import settings
from app.website.forms import ContactForm


template = "pages/contact.html"


# Functions

async def get_context(consumer=None):
    context = get_global_context(consumer=consumer)
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("contact"),
            "title": _("Contact") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("Contact"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "contact",
            "page": template,
            "form": ContactForm(),
        }
    )
    return context


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    # Nav
    await update_active_nav(consumer, "contact")
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
async def send_message(consumer, client_data, lang=None):
    """Send message"""
    form = ContactForm(client_data["data"])
    # Check if form is valid
    if form.is_valid():
        # Nav
        await update_active_nav(consumer, "")
        # Send success message
        html_contact_success = await get_html("forms/contact_success.html")
        data = {
            "action": client_data["action"],
            "selector": "#contact__form",
            "html": html_contact_success,
        }
        await consumer.send_html(data)
        # Send notification
        await send_notification(consumer, _("Contact email sent"), "success")
        # Send email
        send_email(
            subject=_("Contact"),
            to=[form.cleaned_data["email"]],
            template_txt="emails/contact.txt",
            template_html="emails/contact.html",
            data={
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "message": form.cleaned_data["message"],
            },
        )
    else:
        # Send errors
        html = await get_html("forms/contact.html", {"form": form})
        data = {
            "action": client_data["action"],
            "selector": "#contact__form",
            "html": html,
        }
        await consumer.send_html(data)
