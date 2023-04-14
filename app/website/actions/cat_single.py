from channels.db import database_sync_to_async
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    get_html,
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
    try:
        return list(filter(lambda cat: cat.slug == slug, Cat.objects.all()))[0]
    except IndexError:
        return None


async def get_comments(slug):
    cat = await get_cat_from_slug(slug)
    post_id = cat.id
    # Get comments from external API
    response = requests.get(
        "https://jsonplaceholder.typicode.com/comments", {"postId": post_id}
    )
    return response.json()


# Functions


async def get_context(consumer=consumer, slug=None, comments=True):
    context = get_global_context(consumer=consumer)
    # Update context
    cat = await get_cat_from_slug(slug)
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
            "comments": await get_comments(slug) if comments else [],
        }
    )
    return context


@enable_lang
@loading
async def send_page(consumer, client_data, lang=None):
    slug = client_data["data"]["slug"]
    # Nav
    await update_active_nav(consumer, "")
    # Main
    my_context = await get_context(consumer, slug=slug, comments=False)
    html = await get_html(template, my_context)
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": html,
    }
    data.update(my_context)
    await consumer.send_html(data)
    # Comments
    await render_comments(consumer, slug)



async def render_comments(consumer, slug):
    # Render
    html = await get_html("components/_comments.html", {"comments": await get_comments(slug)})
    data = {
        "action": "update_cat->comments",
        "selector": "#comments",
        "html": html,
    }
    await consumer.send_html(data)
