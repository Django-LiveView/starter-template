from django.template.loader import render_to_string
from app.website.context_processors import get_global_context
from app.website.forms import ContactForm
from django.urls import reverse
from django.utils.translation import activate as translation_activate
from django.conf import settings


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
    data = {
        "action": "Update active nav",
        "selector": "#content-header",
        "html": render_to_string("components/_header.html", {"active_nav": page}),
    }
    consumer.send_html(data)
