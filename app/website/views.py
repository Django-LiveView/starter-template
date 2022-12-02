from django.shortcuts import render, redirect
from django.urls import reverse
from app.website.actions.home.view import get_context as get_home_context
from app.website.actions.about_us.view import get_context as get_about_us_context
from app.website.actions.blog_list.view import get_context as get_blog_list_context
from app.website.actions.blog_single.view import get_context as get_blog_single_context
from app.website.actions.project_landing.view import (
    get_context as get_project_landing_context,
)
from app.website.actions.project_category.view import (
    get_context as get_project_category_context,
)
from app.website.actions.project_single.view import (
    get_context as get_project_single_context,
)
from app.website.actions.services.view import get_context as get_services_context
from app.website.actions.contact.view import get_context as get_contact_context
from app.website.actions.privacy_policy.view import (
    get_context as get_privacy_policy_context,
)
from app.website.actions.legal_notice.view import (
    get_context as get_legal_notice_context,
)
from app.website.actions.api import get_post, get_project


def home(request):
    return render(request, "base.html", get_home_context())


def about_us(request):
    return render(request, "base.html", get_about_us_context())


def blog_list(request):
    return render(request, "base.html", get_blog_list_context())


def blog_single(request, slug):
    post = get_post(slug)
    context = get_blog_single_context(post=post)
    context.update({"post": post})
    return render(request, "base.html", context)


def project_landing(request):
    return render(request, "base.html", get_project_landing_context())


def project_category(request, slug):
    return render(request, "base.html", get_project_category_context(slug))


def project_single(request, category, slug):
    return render(request, "base.html", get_project_single_context(category, slug))


def services(request):
    return render(request, "base.html", get_services_context())


def contact(request):
    return render(request, "base.html", get_contact_context())


def privacy_policy(request):
    return render(request, "base.html", get_privacy_policy_context())


def legal_notice(request):
    return render(request, "base.html", get_legal_notice_context())


def page_not_found(request, exception):
    return render(request, "base.html", {"page": "pages/404.html"})


def page_server_error(request):
    return render(request, "base_simple.html", {"page": "pages/500.html"})


def robots(request):
    return render(request, "txts/robots.txt", content_type="text/plain")


def security(request):
    return render(request, "txts/security.txt", content_type="text/plain")


def humans(request):
    return render(request, "txts/humans.txt", content_type="text/plain")
