from django.contrib import admin
from app.website.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
