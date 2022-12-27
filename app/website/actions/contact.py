from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    update_active_nav,
    enable_lang,
    loading,
    send_email,
    send_notification,
)
from core import settings
from app.website.forms import ContactForm


template = "pages/contact.html"


def get_context(consumer=None, lang=None):
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


def get_html(consumer=None, lang=None):
    return render_to_string(template, get_context(consumer=consumer, lang=lang))


@enable_lang
@loading
def send_page(consumer, client_data, lang=None):
    # Nav
    update_active_nav(consumer, "contact")
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
def send_message(consumer, client_data, lang=None):
    """Send message"""
    form = ContactForm(client_data["data"])
    # Check if form is valid
    if form.is_valid():
        # Send success message
        data = {
            "action": client_data["action"],
            "selector": "#contact__form",
            "html": render_to_string("forms/contact_success.html"),
        }
        consumer.send_html(data)
        # Send notification
        send_notification(consumer, _("Contact email sent"), "success")
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
        data = {
            "action": client_data["action"],
            "selector": "#contact__form",
            "html": render_to_string("forms/contact.html", {"form": form}),
        }
        consumer.send_html(data)
