from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
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
from django.core.files.uploadedfile import SimpleUploadedFile


template = "pages/update_cat.html"


def get_context(consumer=None, slug=None, client_data=None, form=None, lang=None):
    context = get_global_context(consumer=consumer)
    list_cats = list(filter(lambda cat: cat.slug == slug, Cat.objects.all()))
    if len(list_cats) > 0:
        cat = list_cats[0]
        form = CatForm(initial={
            "name": cat.name,
            "age": cat.age,
            "biography": cat.biography,
        })
        # Update context
        context.update(
            {
                "url": settings.DOMAIN_URL + reverse("cat update", kwargs={"cat_slug": slug}),
                "title": _("Update cat " + cat.name) + " | " + settings.SITE_NAME,
                "meta": {
                    "description": _("Update a cat"),
                    "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
                },
                "active_nav": "",
                "page": template,
                "cat": cat,
                "form": form,
            }
    )
    return context


def get_html(consumer=None, slug=None, client_data=None, form=None, lang=None):
    return render_to_string(
        template,
        get_context(consumer=consumer, slug=slug, client_data=client_data, form=form, lang=lang),
    )


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
    data.update(get_context())
    consumer.send_html(data)


@enable_lang
@loading
def update(consumer, client_data, lang=None):
    slug = client_data["data"]["slug"]
    # Check if cat exists and if all data is present
    if client_data and "data" in client_data and "form" in client_data["data"]:
        # Add file to input image
        base64_str = client_data["data"]["form"]["avatar"]["base64"]
        mime_type = client_data["data"]["form"]["avatar"]["mimeType"]
        # Create byte file from base64
        my_file_bytes, my_filename = get_image_from_base64(
            base64_str, mime_type, is_file=False
        )
        # Set data in form
        form = CatForm(
            client_data["data"]["form"],
            {
                "avatar": SimpleUploadedFile(
                    my_filename,
                    my_file_bytes,
                    content_type=mime_type,
                )
            } if base64_str else None,
        )
        if form.is_valid():
            # Create cat
            form.save(slug=slug)
            # Send notification
            send_notification(consumer, _("A cat is update!"), "success")
            # Redirect to cats list
            cats.send_page(consumer, client_data, lang=lang)
        else:
            # Send form errors
            data = {
                "action": client_data["action"],
                "selector": "#main",
                "html": get_html(
                    consumer=consumer, slug=slug, client_data=client_data, form=form, lang=lang
                ),
            }
            data.update(get_context())
            consumer.send_html(data)
