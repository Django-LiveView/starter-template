from app.website.actions.home import get_context as get_home_context
from app.website.actions.about_us import get_context as get_about_us_context
from app.website.actions.cats import get_context as get_cats_context
from app.website.actions.cat_single import get_context as get_cat_single_context
from django.shortcuts import render
from django.conf import settings
from app.website.models import Cat


def home(request):
    return render(request, "base.html", get_home_context())


def about_us(request):
    return render(request, "base.html", get_about_us_context())


def cats_list(request):
    return render(request, "base.html", get_cats_context())


def cat_single(request, cat_slug):
    return render(request, "base.html", get_cat_single_context(slug=cat_slug))

def login(request):
    return render(request, "base.html", {"page": "pages/login.html"})

def robots(request):
    return render(request, "txts/robots.txt", content_type="text/plain", context={"DOMAIN": settings.DOMAIN})

def sitemap(request):
    return render(request, "txts/sitemap.txt", content_type="text/plain", context={
        "DOMAIN": settings.DOMAIN,
        "cats": Cat.objects.all(),
    })

def security(request):
    return render(request, "txts/security.txt", content_type="text/plain")


def humans(request):
    return render(request, "txts/humans.txt", content_type="text/plain")

def page_not_found(request, exception):
    return render(request, "base.html", {"page": "pages/404.html"})


def page_server_error(request):
    return render(request, "base_simple.html", {"page": "pages/500.html"})
