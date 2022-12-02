from os import environ
from django.conf import settings
from app.website.forms import ContactForm


def get_global_context():
    """Return a dictionary of global context variables."""
    return {
        "DEBUG": settings.DEBUG,
        "HCAPTCHA_KEY": environ.get("HCAPTCHA_KEY"),
        "GOOGLE_ANALYTICS": environ.get("GOOGLE_ANALYTICS"),
        "COOKIEBOT_KEY": environ.get("COOKIEBOT_KEY"),
        "contact_form": ContactForm(),
        "THUMBOR_URL": settings.THUMBOR_URL + "/unsafe/XsizeX/filters:format(webp)/"
        if settings.THUMBOR_ENABLED
        else "",
    }


def customs(request):
    """Return a dictionary of context variables."""
    return get_global_context()
