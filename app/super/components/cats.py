from django.contrib import admin
from app.website.models import Cat


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
