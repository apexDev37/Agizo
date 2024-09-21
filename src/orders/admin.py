"""Admin module for the `orders` app.

Register models to the Django Admin panel site.
"""

from django.contrib import admin

from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Custom admin interface representation for `Order` model."""

    list_display = (
        "id",
        "customer",
        "created_at",
    )
    list_filter = ("customer", "created_at")
    ordering = ("created_at",)
    readonly_fields = (
        "id",
        "customer",
        "created_at",
    )
    search_fields = ("customer",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Custom admin interface representation for `OrderItem` model."""

    list_display = (
        "id",
        "order",
        "name",
        "price",
        "quantity",
    )
    readonly_fields = (
        "id",
        "order",
        "price",
        "quantity",
    )
    search_fields = (
        "name",
        "order",
    )
