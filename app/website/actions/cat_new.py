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
from app.website.forms import CatForm
from app.website.actions import cats
from django.core.files.uploadedfile import SimpleUploadedFile


template = "pages/new_cat.html"


def get_context(consumer=None, client_data=None, form=None, lang=None):
    context = get_global_context(consumer=consumer)
    # Check client_data["data"]["form"] exist
    if not form:
        form = CatForm()
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("cat new"),
            "title": _("New cat") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("New cat page of the website"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "",
            "page": template,
            "form": form,
        }
    )
    return context


def get_html(consumer=None, client_data=None, form=None, lang=None):
    return render_to_string(
        template,
        get_context(consumer=consumer, client_data=client_data, form=form, lang=lang),
    )


@enable_lang
@loading
def send_page(consumer, client_data, lang=None):
    # Nav
    update_active_nav(consumer, "")
    # Main
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": get_html(consumer=consumer, client_data=client_data, lang=lang),
    }
    data.update(get_context())
    consumer.send_html(data)


@enable_lang
@loading
def create(consumer, client_data, lang=None):
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
            },
        )
        if form.is_valid():
            # Create cat
            form.save()
            # Send notification
            send_notification(consumer, _("A cat is born!"), "success")
            # Redirect to cats list
            cats.send_page(consumer, client_data, lang=lang)
        else:
            # Send form errors
            data = {
                "action": client_data["action"],
                "selector": "#main",
                "html": get_html(
                    consumer=consumer, client_data=client_data, form=form, lang=lang
                ),
            }
            data.update(get_context())
            consumer.send_html(data)
