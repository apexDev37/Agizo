"""Admin module for the `accounts` app.

Register models to the Django Admin panel site.
"""

from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Custom admin interface representation for `User` model."""

    list_display = (
        "email",
        "is_active",
        "is_superuser",
        "created_at",
    )
    list_filter = ("is_active", "is_superuser")
    ordering = ("created_at",)
    readonly_fields = (
        "id",
        "created_at",
    )
    search_fields = ("email",)
