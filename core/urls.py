"""URL Configuration

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
from django.urls import path
from app.website import views
from app.website.feeds import LatestEntriesFeed
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

# Underscore _ for paths that will be translated
urlpatterns = i18n_patterns(
    path("", views.home, name="home"),
    path(_("about-us/"), views.about_us, name="about us"),
    path(_("cats/"), views.cats_list, name="cats list"),
    path(_("cats/<slug:cat_slug>/"), views.cat_single, name="cat single"),
    path(_("login/"), views.login, name="login"),
    path(_("profile/"), views.profile, name="profile"),
    path(_("contact/"), views.contact, name="contact"),
    path(_("feed/"), LatestEntriesFeed(), name="feed"),
    path("robots.txt", views.robots, name="robots"),
    path("humans.txt", views.humans, name="humans"),
    path("security.txt", views.security, name="security"),
    path("sitemap.txt", views.sitemap, name="sitemap"),
    path("admin/", admin.site.urls),
    prefix_default_language=False,
)

handler404 = "app.website.views.page_not_found"
handler500 = "app.website.views.page_server_error"
