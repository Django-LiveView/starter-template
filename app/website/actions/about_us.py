from app.website.actions.utils import set_language
from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.actions.utils import (
    toggle_loading,
    update_active_nav,
    enable_lang,
    loading,
)
from core import settings


template = "pages/about_us.html"


def get_context():
    context = get_global_context()
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


def get_html(lang=None):
    return render_to_string(template, get_context())


@enable_lang
@loading
def send_page(consumer, client_data, lang=None):
    # Nav
    update_active_nav(consumer, "about us")
    # Main
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": get_html(lang=lang),
    }
    data.update(get_context())
    consumer.send_html(data)
