from django.template.loader import render_to_string
from app.website.context_processors import get_global_context
from django.utils.translation import activate as translation_activate
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from uuid import uuid4
from threading import Thread
from time import sleep


def set_language(language="en"):
    """Set the language."""
    if language:
        translation_activate(language)


def enable_lang(func):
    """Decorator: Enable language"""

    def wrapper(*args, **kwargs):
        lang = args[1]["data"].get("lang", settings.LANGUAGE_CODE)
        set_language(lang)
        kwargs["lang"] = lang
        return func(*args, **kwargs)

    return wrapper


def toggle_loading(consumer, show=False):
    """Toogle the footer form."""
    data = {
        "action": ("Show" if show else "Hide") + " loading",
        "selector": "#loading",
        "html": render_to_string("components/_loading.html", get_global_context())
        if show
        else "",
    }
    consumer.send_html(data)


def loading(func):
    """Decorator: Show loading."""

    def wrapper(*args, **kwargs):
        toggle_loading(args[0], True)
        result = func(*args, **kwargs)
        toggle_loading(args[0], False)
        return result

    return wrapper


def update_active_nav(consumer, page):
    """Update the active nav item in the navbar."""
    context = get_global_context(consumer=consumer)
    context["active_nav"] = page
    data = {
        "action": "Update active nav",
        "selector": "#content-header",
        "html": render_to_string("components/_header.html", context),
    }
    consumer.send_html(data)


def send_email(
    subject="", to=[], template_txt="", template_html="", data={}, attachments=[]
):
    """Send email"""
    msg = EmailMultiAlternatives(
        subject,
        render_to_string(template_txt, data | {"settings": settings}),
        settings.DEFAULT_FROM_EMAIL,
        to,
    )
    msg.attach_alternative(
        render_to_string(template_html, data | {"settings": settings}), "text/html"
    )
    for attachment in attachments:
        msg.attach_file(attachment)
    return msg.send()


def send_notification(consumer: object, message: str, level: str = "info"):
    """Send notification."""
    # Variables
    uuid = str(uuid4())
    timeout = 3000  # ms
    # Show message
    data = {
        "action": "new_notification",
        "selector": "#notifications",
        "html": render_to_string(
            "components/_notification.html",
            {
                "id": uuid,
                "message": message,
                "level": level,
            },
        ),
        "append": True,
    }
    consumer.send_html(data)
    # Remove message async
    def remove_notification(consumer, uuid):
        # Sleep timeout
        sleep(timeout / 1000)
        data = {
            "action": "delete_notification",
            "selector": f"#notifications > #notifications__item-{uuid}",
            "html": "",
        }
        consumer.send_html(data)

    Thread(target=remove_notification, args=(consumer, uuid)).start()
