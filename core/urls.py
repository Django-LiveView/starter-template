"""ccstech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.website import views
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

# Underscore _ for paths that will be translated
urlpatterns = i18n_patterns(
    path("", views.home, name="home"),
    # Prometheus
    path("", include("django_prometheus.urls")),
    path(_("nosotros") + "/", views.about_us, name="about us"),
    path(_("servicios") + "/", views.services, name="services"),
    path(_("blog") + "/", views.blog_list, name="blog list"),
    path(_("blog") + "/<slug:slug>/", views.blog_single, name="blog single"),
    path(_("proyectos") + "/", views.project_landing, name="projects landing"),
    path(
        _("proyectos") + "/<slug:slug>/",
        views.project_category,
        name="projects category",
    ),
    path(
        _("proyectos") + "/<slug:category>/<slug:slug>/",
        views.project_single,
        name="project single",
    ),
    path(_("contacto") + "/", views.contact, name="contact"),
    path(
        _("politica-de-privacidad") + "/", views.privacy_policy, name="privacy policy"
    ),
    path(_("aviso-legal") + "/", views.legal_notice, name="legal notice"),
    path("robots.txt", views.robots, name="robots"),
    path("security.txt", views.security, name="security"),
    path("humans.txt", views.humans, name="humans"),
    prefix_default_language=False,
)

handler404 = "app.website.views.page_not_found"
handler500 = "app.website.views.page_server_error"
