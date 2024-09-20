"""View tests for the `accounts` app.

Prefer to mark all REST API endpoint tests as `integration` tests.
Whenever possible, prefer to use DRF over standard Django test tools.

For more details about testing views
See (Django): https://docs.djangoproject.com/en/4.2/topics/testing/tools/#the-test-client
See (DRF): https://www.django-rest-framework.org/api-guide/testing/
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

# Leverage global variable to apply custom marker at the module level
# for all tests. Add markers by assigning values of type: list.
# For example: [pytest.mark.smoke, pytest.mark.unit, ...]
pytestmark = pytest.mark.integration

CUSTOMER_ENDPOINT: str = reverse("accounts:create_customer")


@pytest.fixture()
def client() -> APIClient:
    client = APIClient()
    client.headers = {
        "Content-Type": "application/json",
    }
    client.raise_request_exception = True
    return client


def test_should_return_400_for_invalid_customer_request_data(client: APIClient) -> None:
    # Given
    payload = _test_data(user_email="nonexistent", user_password="tooshort")

    # When
    response = client.post(path=CUSTOMER_ENDPOINT, data=payload)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["user_email"], response.data["user_password"]
    assert all(isinstance(v[0], ErrorDetail) for v in response.data.values())


@pytest.mark.django_db()
def test_should_return_201_on_created_user_and_customer_profile(
    client: APIClient,
) -> None:
    # Given
    payload = _test_data()

    # When
    response = client.post(path=CUSTOMER_ENDPOINT, data=payload)

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == "success"
    assert response.data["customer"]["email"] == payload["user_email"]


# ==============================================================================
# Helper functions.
# ==============================================================================


def _test_data(
    name: str = "John Doe",
    phone_number: str = "+245000000000",
    user_email: str = "johndoe@email.example",
    user_password: str = "jd-secret-pwd",
) -> dict[str, str]:
    """Represents a valid payload to create a customer.

    Note:
        - Override data by passing arguments to the func params with defaults.
        Invalid values can be passed as arguments allowing the func signature
        to clearly express fields that will fail validation.
    """
    return {
        "name": name,
        "phone_number": phone_number,
        "user_email": user_email,
        "user_password": user_password,
    }
