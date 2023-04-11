from django.template.loader import render_to_string
from channels.db import database_sync_to_async
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
import requests


template = "pages/single_cat.html"

# Database


@database_sync_to_async
def get_cat_from_slug(slug):
    return list(filter(lambda cat: cat.slug == slug, Cat.objects.all()))


async def get_comments(slug):
    list_cats = await get_cat_from_slug(slug)
    post = list_cats[0]
    post_id = post.id
    # Get comments from external API
    response = requests.get(
        "https://jsonplaceholder.typicode.com/comments", {"postId": post_id}
    )
    return response.json()


# Functions


async def get_context(lang=None, slug=None, comments=True):
    context = get_global_context()
    list_cats = await get_cat_from_slug(slug)
    if len(list_cats) > 0:
        cat = list_cats[0]
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL
            + reverse("cat single", kwargs={"cat_slug": slug}),
            "title": cat.name + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("All cats page"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "",
            "page": template,
            "cat": cat,
            "comments": await get_comments(slug) if comments else None,
        }
    )
    return context


async def get_html(lang=None, slug=None):
    return render_to_string(
        template, await get_context(lang=lang, slug=slug, comments=False)
    )


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    slug = client_data["data"]["slug"]
    # Nav
    await update_active_nav(consumer, "")
    # Main
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": await get_html(lang=lang, slug=slug),
    }
    data.update(await get_context(lang=lang, slug=slug, comments=False))
    await consumer.send_html(data)
    # Comments
    await render_comments(consumer, slug)


async def render_comments(consumer, slug):
    comments = await get_comments(slug)
    # Render
    data = {
        "action": "update_cat->comments",
        "selector": "#comments",
        "html": render_to_string("components/_comments.html", {"comments": comments}),
    }
    await consumer.send_html(data)
