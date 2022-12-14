from app.website.actions.utils import set_language
from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.actions.utils import (
    toggle_loading,
    update_active_nav,
)
from core import settings
from app.website.models import Cat


template = "pages/all_cats.html"


def get_context(lang=None):
    context = get_global_context()
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("all cats"),
            "title": _("Cats") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _(
                    "All cats page"
                ),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "all cats",
            "page": template,
            "cats": Cat.objects.all(),
        }
    )
    return context


def get_html(lang=None):
    return render_to_string(template, get_context(lang=lang))


def send_page(consumer, client_data):
    # Set language
    lang = client_data["data"].get("lang", settings.LANGUAGE_CODE)
    set_language(lang)
    # Show loading
    toggle_loading(consumer, True)
    # Nav
    update_active_nav(consumer, "all cats")
    # Main
    data = {"action": client_data["action"], "selector": "#main", "html": get_html(lang=lang)}
    data.update(get_context(lang=lang))
    consumer.send_html(data)
    # Hide loading
    toggle_loading(consumer, False)
