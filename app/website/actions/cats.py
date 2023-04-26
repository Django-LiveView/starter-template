from django.templatetags.static import static
from channels.db import database_sync_to_async
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    get_html,
    update_active_nav,
    enable_lang,
    send_notification,
    loading,
)
from core import settings
from app.website.models import Cat


template = "pages/all_cats.html"
elements_per_page = 3

# Database


@database_sync_to_async
def get_all_cats(start=None, limit=None):
    my_cats = Cat.objects.all().order_by("-id")
    if start and limit:
        return tuple(my_cats[start:limit])
    if limit:
        return tuple(my_cats[:limit])
    return tuple(my_cats)


@database_sync_to_async
def delete_cat(slug):
    cats = Cat.objects.all()
    for cat in cats:
        if cat.slug == slug:
            cat.delete()


@database_sync_to_async
def is_last_page(page=1, elements_per_page=3):
    return Cat.objects.all().count() // elements_per_page < page


# Functions


async def get_context(consumer=None, lang=None):
    context = get_global_context(consumer=consumer)
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
            "cats": await get_all_cats(limit=elements_per_page),
            "pagination": 1,
        }
    )
    return context


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    # Nav
    await update_active_nav(consumer, "all cats")
    # Main
    my_context = await get_context(consumer=consumer)
    html = await get_html(template, my_context)
    data = {"action": client_data["action"], "selector": "#main", "html": html}
    data.update(my_context)
    await consumer.send_html(data)


# Pagination


@enable_lang
@loading
async def send_cats_per_page(consumer, client_data, lang=None, page=1):
    """Send cats per page"""
    # Get current page
    if page in client_data["data"]:
        my_page = client_data["data"]["page"]
    else:
        my_page = page
    start = (my_page - 1) * elements_per_page
    end = start + elements_per_page
    # Update list of cats
    my_context = get_global_context(consumer=consumer)
    my_context_list_cats = my_context.copy()
    my_context_list_cats.update(
        {
            "cats": await get_all_cats(start=start, limit=end),
            "pagination": my_page,
            "is_last_page": await is_last_page(
                page=my_page, elements_per_page=elements_per_page
            ),
        }
    )
    html_list_cats = await get_html("components/_list_cats.html", my_context_list_cats)
    data = {
        "action": client_data["action"],
        "selector": "#list-cats",
        "html": html_list_cats,
    }

    await consumer.send_html(data)
    # Update pagination
    my_context_paginator = my_context.copy()
    my_context_paginator.update(
        {
            "pagination": my_page,
            "is_last_page": await is_last_page(my_page),
        }
    )
    html = await get_html("components/_paginator.html", my_context_paginator)
    data = {"action": "update_pagination", "selector": "#paginator", "html": html}
    await consumer.send_html(data)


@enable_lang
@loading
async def next_page(consumer, client_data, lang=None):
    """Next page"""
    page = int(client_data["data"]["pagination"])
    await send_cats_per_page(consumer, client_data, lang=lang, page=page + 1)


@enable_lang
@loading
async def previous_page(consumer, client_data, lang=None):
    """Prev page"""
    page = int(client_data["data"]["pagination"])
    await send_cats_per_page(consumer, client_data, lang=lang, page=page - 1)


@enable_lang
@loading
async def delete(consumer, client_data, lang=None):
    """Delete cat"""
    # Delete cat
    await delete_cat(client_data["data"]["slug"])
    # Notify
    await send_notification(
        consumer, _("A cat has died! it has 6 lives left."), "danger"
    )
    # Refresh page
    await send_page(consumer, client_data, lang=lang)
