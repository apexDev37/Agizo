"""View tests for the `accounts` app.

Prefer to mark all REST API endpoint tests as `integration` tests.
Whenever possible, prefer to use DRF over standard Django test tools.

Note:
    - Given no mechanism to pass valid OAuth2 tokens from an OIDC auth flow as
    credentials to the API test client, we simply force authenticate.

For more details about testing views
See (Django): https://docs.djangoproject.com/en/4.2/topics/testing/tools/#the-test-client
See (DRF): https://www.django-rest-framework.org/api-guide/testing/
"""

from collections.abc import Generator
from typing import TypeAlias, TypeVar

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

# Leverage global variable to apply custom marker at the module level
# for all tests. Add markers by assigning values of type: list.
# For example: [pytest.mark.smoke, pytest.mark.unit, ...]
pytestmark = [pytest.mark.integration, pytest.mark.django_db]

CUSTOMER_ENDPOINT: str = reverse("accounts:create_customer")

# typing.
T = TypeVar("T")
TGenerator: TypeAlias = Generator[T, None, None]

User = get_user_model()


@pytest.fixture()
def client() -> APIClient:
    """Represents an API client from DRF's test utilities."""
    client = APIClient()
    client.headers = {
        "Content-Type": "application/json",
    }
    client.raise_request_exception = True
    return client


@pytest.fixture()
def user() -> TGenerator[AbstractBaseUser]:
    """Represents a user instance persisted in the DB."""
    user = User.objects.create_user(
        email="johndoe@email.example", password="jd-secret-pwd"
    )
    yield user
    user.delete()


@pytest.fixture()
def auth_client(client: APIClient, user: AbstractBaseUser) -> TGenerator[APIClient]:
    """Represents an authenticated API client from DRF's test utilities."""
    client.force_authenticate(user=user)
    yield client
    client.force_authenticate(user=None)


def test_should_return_401_for_unauthenticated_client_requests(
    client: APIClient,
) -> None:
    # Given
    payload = _test_data()

    # When
    response = client.post(path=CUSTOMER_ENDPOINT, data=payload)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "not_authenticated" in response.data["detail"].code


def test_should_return_400_for_invalid_customer_request_data(
    auth_client: APIClient,
) -> None:
    # Given
    payload = _test_data(user_email="nonexistent", user_password="tooshort")

    # When
    response = auth_client.post(path=CUSTOMER_ENDPOINT, data=payload)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["user_email"], response.data["user_password"]
    assert all(isinstance(v[0], ErrorDetail) for v in response.data.values())


def test_should_return_201_on_created_user_and_customer_profile(
    auth_client: APIClient,
) -> None:
    # Given
    payload = _test_data()

    # When
    response = auth_client.post(path=CUSTOMER_ENDPOINT, data=payload)

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == "success"
    assert response.data["customer"]["email"] == payload["user_email"]


# ==============================================================================
# Helper functions.
# ==============================================================================


def _test_data(
    name: str = "Anna blue",
    phone_number: str = "+245000000000",
    user_email: str = "annablue@email.example",
    user_password: str = "ab-secret-pwd",
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
