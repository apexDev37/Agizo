"""Serializer tests for the `orders` app.

Tests to verify serializer-related data validation and DB transactions.
Validation tests should be marked as `unit` tests. Note that some serializer
tests require DB access.

For more details about serializers
See: https://www.django-rest-framework.org/api-guide/serializers/
"""

from typing import TypedDict

import pytest
from django.contrib.auth import get_user_model
from rest_framework import serializers

from orders.serializers import CreateOrderSerializer, OrderItemSerializer

User = get_user_model()


class TOrderItem(TypedDict):
    """Type structure for a single order item data."""

    name: str
    price: float
    quantity: int


class TOrder(TypedDict):
    """Type structure for a single customer order data."""

    items: list[TOrderItem]
    phone_number: str


@pytest.mark.unit
@pytest.mark.parametrize("quantity", [0, -1])
def test_should_validate_order_item_quantity_is_greater_or_equal_to_one(
    quantity: int,
) -> None:
    # Given
    item = TOrderItem(name="Product A1", price=12.50, quantity=quantity)

    with pytest.raises(serializers.ValidationError, match="min_value"):  # Then
        OrderItemSerializer(data=item).is_valid(raise_exception=True)  # When


@pytest.mark.unit
@pytest.mark.parametrize("price", [0, -10.05, 4.99])
def test_should_validate_each_order_item_price_meets_required_price_minimum(
    price: int,
) -> None:
    # Given
    item = TOrderItem(name="Product A1", price=price, quantity=2)

    with pytest.raises(serializers.ValidationError, match="min_value"):  # Then
        OrderItemSerializer(data=item).is_valid(raise_exception=True)  # When


@pytest.mark.unit
def test_should_validate_customer_order_contains_one_or_more_order_items() -> None:
    # Given
    data = TOrder(items=[], phone_number="+254700000000")

    with pytest.raises(serializers.ValidationError, match="empty"):  # Then
        CreateOrderSerializer(data=data).is_valid(raise_exception=True)  # When
