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
import base64
import time
from django.core.files import File
from tempfile import NamedTemporaryFile


template = "pages/profile.html"


def get_context(consumer=None, lang=None):
    context = get_global_context(consumer=consumer)
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("profile"),
            "title": _("Profile") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("Profile"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "profile",
            "page": template,
        }
    )
    return context


def get_html(consumer=None, lang=None):
    return render_to_string(template, get_context(consumer=consumer, lang=lang))


@enable_lang
@loading
def send_page(consumer, client_data, lang=None):
    # Nav
    update_active_nav(consumer, "profile")
    # Main
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": get_html(consumer, lang=lang),
    }
    data.update(get_context(consumer=consumer, lang=lang))
    consumer.send_html(data)


@loading
def update_avatar(consumer, client_data):
    if "mimeType" in client_data["data"] and client_data["data"]["mimeType"] in (
        "image/jpeg",
        "image/png",
        "image/webp",
    ):
        # Variables
        user = consumer.scope["user"]
        avatar_base64 = client_data["data"]["base64"]
        extension = client_data["data"]["mimeType"].split("/")[-1]
        # Str base64 to bytes
        base64_img_bytes = avatar_base64.encode("utf-8")
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        # Bytes to file
        my_filename = f"{user.username}-{int(time.time())}.{extension}"
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(decoded_image_data)
        img_temp.flush()
        my_file = File(img_temp)
        # Update avatar
        user.profile.avatar.save(my_filename, my_file)
        # Update HTML
        data = {
            "action": "update_avatar",
            "selector": "#avatar__container",
            "html": render_to_string("components/_avatar.html", {"user": user}),
        }
        consumer.send_html(data)
    else:
        # Bad extension image
        pass
