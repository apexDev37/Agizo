"""Model tests for the `orders` app.

Tests to verify model-related data validation and DB transaction concerns.
"""

from decimal import Decimal
from typing import TypedDict

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

from accounts.profiles import CustomerProfile
from orders.models import Order, OrderItem

TEST_USER_NAME: str = "John Doe"
TEST_USER_EMAIL: str = "johndoe@email.example"
TEST_USER_PASSWORD: str = "jd-secret-pwd"
TEST_USER_PHONE_NO: str = "+245000000000"

User = get_user_model()


@pytest.fixture
def user() -> AbstractBaseUser:
    return User.objects.create_user(email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD)


@pytest.fixture
def customer(user: AbstractBaseUser) -> CustomerProfile:
    return CustomerProfile.objects.create(
        user=user, name=TEST_USER_NAME, phone_number=TEST_USER_PHONE_NO
    )


@pytest.fixture
def order(customer: CustomerProfile) -> Order:
    return Order.objects.create(customer=customer)


@pytest.mark.unit
def test_should_compute_amount_for_a_single_order_item() -> None:
    # Given
    item = OrderItem(name="Product A", price=100, quantity=3)
    expected = 300

    # When
    actual = item.amount

    # Then
    assert isinstance(actual, Decimal)
    assert actual == expected


class TOrderItem(TypedDict):
    """Type structure for a single order item data."""

    name: str
    price: float
    quantity: int


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("items", "expected"),
    [
        (
            [  # First test case
                TOrderItem(name="Product A", price=10, quantity=3),
                TOrderItem(name="Product B", price=20, quantity=1),
                TOrderItem(name="Product C", price=15, quantity=2),
            ],
            80,
        ),
        (
            [  # Second test case
                TOrderItem(name="Product D", price=19.30, quantity=3),
                TOrderItem(name="Product E", price=35.99, quantity=4),
                TOrderItem(name="Product F", price=11.50, quantity=10),
            ],
            316.86,
        ),
    ],
)
def test_should_compute_total_amount_for_a_given_customer_order(
    order: Order, items: list[TOrderItem], expected: int
) -> None:
    # Given
    _ = [OrderItem.objects.create(order=order, **item) for item in items]

    # When
    actual = order.total_amount

    # Then
    assert isinstance(actual, Decimal)
    assert actual == round(Decimal(expected), 2)
