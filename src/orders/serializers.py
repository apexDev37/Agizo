"""Serializers for the `orders` app.

Define serializers to support data validation and serialization/deserialization
for `orders.models`.

For more details about this file
See: https://www.django-rest-framework.org/api-guide/serializers/
"""

from collections.abc import MutableMapping
from decimal import Decimal
from typing import Any

from rest_framework import serializers

from accounts.profiles import CustomerProfile
from orders.models import Order, OrderItem
from orders.services import OrdersSMSService
from orders.utils import init_africastalking_sms_service


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer to serialize/deserialize `OrderItem` instances."""

    class Meta:  # noqa: D106
        model = OrderItem
        fields = (
            "name",
            "price",
            "quantity",
        )
        extra_kwargs = {
            "name": {"required": True},
            "price": {"required": True, "min_value": round(Decimal(5), 2)},
            "quantity": {"required": True, "min_value": 1},
        }


class CreateOrderSerializer(serializers.ModelSerializer):
    """Serializer to serialize/deserialize `Order` instances.

    Note:
        - The following extra fields have been included as being crucial to
        the process of creating an order: `items` and `customer_phone_number`.
    """

    items = OrderItemSerializer(
        many=True, allow_empty=False, min_length=1, write_only=True
    )
    customer_phone_number = serializers.CharField(min_length=10)

    class Meta:  # noqa: D106
        model = Order
        fields = ("customer_phone_number", "items")
        read_only_fields = ("customer_phone_number",)
        extra_kwargs = {
            "customer": {"write_only": True},
        }

    def create(self, validated_data: MutableMapping[str, Any]) -> Order:
        phone_number = validated_data.pop("customer_phone_number")
        customer = CustomerProfile.objects.filter(phone_number=phone_number).first()

        order = Order.objects.create(customer=customer)

        items = validated_data.pop("items")
        _ = OrderItem.objects.bulk_create(
            [OrderItem(order=order, **item) for item in items]
        )

        sms_client = init_africastalking_sms_service()

        # Push SMS notification to customer who created order.
        service = OrdersSMSService(client=sms_client)
        _ = service.notify_customer(customer)

        return order
