from django.contrib.auth.models import User
from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active")
    exclude = (
        "password",
        "last_session",
        "user_permissions",
        "representedgroup",
        "last_login",
        "groups",
    )
