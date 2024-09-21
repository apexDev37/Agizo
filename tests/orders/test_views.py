"""View tests for the `orders` app.

Prefer to mark all REST API endpoint tests as `integration` tests.
Whenever possible, prefer to use DRF over standard Django test tools.

Note:
    - Validation tests for API data are defined and handled at the serializer
    level as unit tests. See: `test_serializers` module.

For more details about testing views
See (Django): https://docs.djangoproject.com/en/4.2/topics/testing/tools/#the-test-client
See (DRF): https://www.django-rest-framework.org/api-guide/testing/
"""

from typing import TypedDict

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.profiles import CustomerProfile

# Leverage global variable to apply custom marker at the module level
# for all tests. Add markers by assigning values of type: list.
# For example: [pytest.mark.smoke, pytest.mark.unit, ...]
pytestmark = pytest.mark.integration

ORDER_ENDPOINT: str = reverse("orders:create_order")

TEST_USER_NAME: str = "John Doe"
TEST_USER_EMAIL: str = "johndoe@email.example"
TEST_USER_PASSWORD: str = "jd-secret-pwd"
TEST_USER_PHONE_NO: str = "+245000000000"

User = get_user_model()


@pytest.fixture()
def user() -> AbstractBaseUser:
    return User.objects.create_user(email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD)


@pytest.fixture()
def customer(user: AbstractBaseUser) -> CustomerProfile:
    return CustomerProfile.objects.create(
        user=user, name=TEST_USER_NAME, phone_number=TEST_USER_PHONE_NO
    )


@pytest.fixture()
def client() -> APIClient:
    client = APIClient()
    client.headers = {
        "Content-Type": "application/json",
    }
    client.raise_request_exception = True
    return client


class TOrderItem(TypedDict):
    """Type structure for a single order item data."""

    name: str
    price: float
    quantity: int


class TOrder(TypedDict):
    """Type structure for a single customer order data."""

    items: list[TOrderItem]
    customer_phone_number: str


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "items",
    [
        (
            TOrderItem(name="Product A", price=10.05, quantity=2),
            TOrderItem(name="Product B", price=25.00, quantity=1),
            TOrderItem(name="Product C", price=7.50, quantity=4),
        ),
    ],
)
def test_should_create_and_persist_customer_order_with_order_items(
    client: APIClient, customer: CustomerProfile, items: list[TOrderItem]
) -> None:
    # Given
    payload = TOrder(items=items, customer_phone_number=customer.phone_number)

    # When
    response = client.post(path=ORDER_ENDPOINT, data=payload)

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == "success"
    assert response.data["order"]["customer"]["phone_number"] == customer.phone_number
