import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from app.website.models import Cat

# Load all context functions
path = os.getcwd()
for entry in os.scandir(os.path.join(path, "app", "website", "actions")):
    if entry.is_file():
        name = entry.name.split(".")[0]
        exec(
            f"from app.website.actions.{name} import get_context as get_{name}_context"
        )


async def home(request):
    return render(request, "base.html", await get_home_context())


async def about_us(request):
    return render(request, "base.html", await get_about_us_context())


async def cats_list(request):
    return render(request, "base.html", await get_cats_context())


async def cat_single(request, cat_slug):
    return render(request, "base.html", await get_cat_single_context(slug=cat_slug))


@login_required(login_url="login")
async def cat_new(request):
    return render(request, "base.html", await get_cat_new_context())


@login_required(login_url="login")
async def cat_update(request, cat_slug):
    return render(request, "base.html", await get_cat_update_context(slug=cat_slug))


async def login(request):
    return render(request, "base.html", await get_login_context())


@login_required(login_url="login")
async def profile(request):
    return render(request, "base.html", await get_profile_context())


async def contact(request):
    return render(request, "base.html", await get_contact_context())


def robots(request):
    return render(
        request,
        "txts/robots.txt",
        content_type="text/plain",
        context={"DOMAIN": settings.DOMAIN},
    )


def sitemap(request):
    return render(
        request,
        "txts/sitemap.txt",
        content_type="text/plain",
        context={
            "DOMAIN": settings.DOMAIN,
            "cats": Cat.objects.all(),
        },
    )


def security(request):
    return render(request, "txts/security.txt", content_type="text/plain")


def humans(request):
    return render(request, "txts/humans.txt", content_type="text/plain")


def page_not_found(request, exception):
    return render(request, "base.html", {"page": "pages/404.html"})


def page_server_error(request):
    return render(request, "base_simple.html", {"page": "pages/500.html"})
