from django.contrib import admin
from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)

from app.super.components.users import UserAdmin
from app.super.components.cats import CatAdmin
from app.super.components.clients import ClientAdmin
