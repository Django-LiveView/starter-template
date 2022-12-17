from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.actions.utils import (
    update_active_nav,
    enable_lang,
    loading,
)
from core import settings
from app.website.models import Cat


template = "pages/all_cats.html"
elements_per_page = 3


def get_context(lang=None):
    context = get_global_context()
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("cats list"),
            "title": _("Cats") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("All cats page"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "all cats",
            "page": template,
            "cats": Cat.objects.all().order_by("-id")[:3],
            "pagination": 1,
        }
    )
    return context


def get_html(lang=None):
    return render_to_string(template, get_context(lang=lang))


@enable_lang
@loading
def send_page(consumer, client_data, lang=None):
    # Nav
    update_active_nav(consumer, "all cats")
    # Main
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": get_html(lang=lang),
    }
    data.update(get_context(lang=lang))
    consumer.send_html(data)


# Pagination


def is_last_page(page=1):
    return Cat.objects.all().count() // elements_per_page < page


@enable_lang
@loading
def send_cats_per_page(consumer, client_data, lang=None, page=1):
    """Send cats per page"""
    # Get current page
    if page in client_data["data"]:
        my_page = client_data["data"]["page"]
    else:
        my_page = page
    start = (my_page - 1) * elements_per_page
    end = start + elements_per_page
    # Update list of cats
    data = {
        "action": client_data["action"],
        "selector": "#list-cats",
        "html": render_to_string(
            "components/_list_cats.html",
            {
                "cats": Cat.objects.all().order_by("-id")[start:end],
                "pagination": my_page,
                "is_last_page": is_last_page(my_page),
            },
        ),
    }
    consumer.send_html(data)
    # Update pagination
    data = {
        "action": "update_pagination",
        "selector": "#paginator",
        "html": render_to_string(
            "components/_paginator.html",
            {
                "pagination": my_page,
                "is_last_page": is_last_page(my_page),
            },
        ),
    }
    consumer.send_html(data)


@enable_lang
@loading
def next_page(consumer, client_data, lang=None):
    """Next page"""
    page = int(client_data["data"]["pagination"])
    send_cats_per_page(consumer, client_data, lang=lang, page=page + 1)


@enable_lang
@loading
def previous_page(consumer, client_data, lang=None):
    """Prev page"""
    page = int(client_data["data"]["pagination"])
    send_cats_per_page(consumer, client_data, lang=lang, page=page - 1)
