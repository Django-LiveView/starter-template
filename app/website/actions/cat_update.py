from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    get_html,
    update_active_nav,
    send_notification,
    enable_lang,
    loading,
    get_image_from_base64,
)
from core import settings
from app.website.models import Cat
from app.website.forms import CatForm
from app.website.actions import cats
from app.website.actions.cat_single import get_cat_from_slug
from django.core.files.uploadedfile import SimpleUploadedFile


template = "pages/update_cat.html"

# Database


# Functions


async def get_context(consumer=None, slug=None, form=None):
    context = get_global_context(consumer=consumer)
    cat = await get_cat_from_slug(slug)
    if cat:
        if not form:
            form = CatForm(
                initial={
                    "name": cat.name,
                    "age": cat.age,
                    "biography": cat.biography,
                }
            )
        # Update context
        context.update(
            {
                "url": settings.DOMAIN_URL
                + reverse("cat update", kwargs={"cat_slug": slug}),
                "title": _("Update cat " + cat.name) + " | " + settings.SITE_NAME,
                "meta": {
                    "description": _("Update a cat"),
                    "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
                },
                "active_nav": "",
                "page": template,
                "cat": cat,
                "slug": slug,
                "form": form,
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
    my_context = await get_context(consumer=consumer, slug=slug)
    html = await get_html(template, my_context)
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": html,
    }

    await consumer.send_html(data)


@enable_lang
@loading
async def update(consumer, client_data, lang=None):
    slug = client_data["data"]["slug"]
    # Check if cat exists and if all data is present
    if client_data and "data" in client_data and "form" in client_data["data"]:
        # Add file to input image
        base64_str = client_data["data"]["form"]["avatar"]["base64"]
        mime_type = client_data["data"]["form"]["avatar"]["mimeType"]
        is_new_avatar = base64_str and mime_type
        if is_new_avatar:
            # Create byte file from base64
            my_file_bytes, my_filename = get_image_from_base64(
                base64_str, mime_type, is_file=False
            )
            new_uploaded_file = SimpleUploadedFile(
                my_filename,
                my_file_bytes,
                content_type=mime_type,
            )
        # Update data in form
        form = CatForm(
            client_data["data"]["form"],
            {
                "avatar": new_uploaded_file,
            }
            if is_new_avatar
            else None,
        )
        # Disable required field for avatar
        form.fields["avatar"].required = False

        # Check if form is valid
        if form.is_valid():
            # Create cat
            await form.save(slug=slug)
            # Send notification
            await send_notification(consumer, _("A cat is update!"), "success")
            # Redirect to cats list
            await cats.send_page(consumer, client_data, lang=lang)
        else:
            # Send form errors
            slug = client_data["data"]["slug"]
            my_context = await get_context(consumer=consumer, slug=slug, form=form)
            html = await get_html(template, my_context)
            data = {
                "action": client_data["action"],
                "selector": "#main",
                "html": html,
            }
            data.update(my_context)
            await consumer.send_html(data)
