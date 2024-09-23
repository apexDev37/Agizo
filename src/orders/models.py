"""Models for the `orders` app."""

from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils.functional import cached_property

from accounts.profiles import CustomerProfile


class Order(models.Model):
    """Represents a single order made by a customer.

    Note:
        - Given the API's write over read orientation, a performance tradeoff is
        made to dynamically compute `total_amount` instead of persisting the
        field (denormalization). This also keeps things simple.
    """

    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="The customer who placed this order.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # noqa: D106
        verbose_name = "order"
        verbose_name_plural = "orders"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return (
            f"id: {self.id} "
            f"customer: {self.customer.user.email} "
            f"amount: {self.total_amount}"
        )

    @cached_property
    def total_amount(self) -> Decimal:
        """Compute the total amount for all order items."""
        total = (
            self.items.aggregate(total=Sum(models.F("price") * models.F("quantity")))[
                "total"
            ]
            or 0
        )
        return round(Decimal(total), 2)


class OrderItem(models.Model):
    """Represents a single item part of a customer order.

    Note:
        - The fields `name` and `price` are related to a given product.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        help_text="The order to which this item belongs.",
    )
    name = models.CharField(
        blank=False,
        max_length=50,
        null=False,
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    quantity = models.PositiveSmallIntegerField()

    class Meta:  # noqa: D106
        verbose_name = "order_item"
        verbose_name_plural = "order_items"
        ordering = ["-price"]

    def __str__(self) -> str:
        return f"id: {self.id}: price: {self.price} quantity: {self.quantity}"

    @cached_property
    def amount(self) -> Decimal:
        """Compute the amount for an order item."""
        amount = self.price * self.quantity
        return round(Decimal(amount), 2)
