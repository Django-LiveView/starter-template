from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    update_active_nav,
    enable_lang,
    loading,
)
from core import settings
from app.website.models import Cat


template = "pages/single_cat.html"


def get_context(lang=None, slug=None):
    context = get_global_context()
    list_cats = list(filter(lambda cat: cat.slug == slug, Cat.objects.all()))
    if len(list_cats) > 0:
        cat = list_cats[0]
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("cats list"),
            "title": cat.name + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("All cats page"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "",
            "page": template,
            "cat": cat,
        }
    )
    return context


def get_html(lang=None, slug=None):
    return render_to_string(template, get_context(lang=lang, slug=slug))


@enable_lang
@loading
def send_page(consumer, client_data, lang=None):
    slug = client_data["data"]["slug"]
    # Nav
    update_active_nav(consumer, "")
    # Main
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": get_html(lang=lang, slug=slug),
    }
    data.update(get_context(lang=lang, slug=slug))
    consumer.send_html(data)
