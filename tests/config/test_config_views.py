"""View tests for the project.

Whenever possible, prefer to use DRF over standard Django test tools.

For more details about testing views
See (Django): https://docs.djangoproject.com/en/4.2/topics/testing/tools/#the-test-client
See (DRF): https://www.django-rest-framework.org/api-guide/testing/
"""

from collections.abc import Callable, Generator
from typing import Any, TypeAlias, TypeVar

import pytest
from django.db import connections
from django.urls import reverse
from psycopg import OperationalError as PsycopgOperationalError
from rest_framework import status
from rest_framework.test import APIClient

# typing.
T = TypeVar("T")
TGenerator: TypeAlias = Generator[T, None, None]

HEALTH_CHECK_ENDPOINT: str = reverse("health_check")


# Leverage global variable to apply custom marker at the module level
# for all tests. Add markers by assigning values of type: list.
# For example: [pytest.mark.smoke, pytest.mark.unit, ...]
pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
]


@pytest.fixture
def client() -> APIClient:
    """Represents an API client from DRF's test utils."""
    client = APIClient()
    client.headers = {
        "Content-Type": "application/json",
    }
    client.raise_request_exception = True
    return client


@pytest.fixture
def mock_db_conn_failure() -> Callable[[], pytest.MonkeyPatch]:
    """Mocks a database connection failure at the connection level."""

    def _mock_failure() -> pytest.MonkeyPatch:
        def mock_connect(*args: Any, **kwargs: Any) -> None:
            errmsg = "Simulated connection error"
            raise PsycopgOperationalError(errmsg)

        mp = pytest.MonkeyPatch()

        # [Crucial] close any existing connection before mocking!
        if "default" in connections:
            connections["default"].close()

        mp.setattr(connections["default"].connection.__class__, "connect", mock_connect)
        return mp

    return _mock_failure


def test_should_return_200_okay_as_default_response(
    # Given
    client: APIClient,
) -> None:
    # When
    response = client.get(path=HEALTH_CHECK_ENDPOINT)

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert "healthy" in response.data["status"]


def test_should_return_503_unavailable_when_unable_to_connect_to_db(
    client: APIClient,
    mock_db_conn_failure: Callable[[], pytest.MonkeyPatch],
) -> None:
    # Given
    mp = mock_db_conn_failure()

    with mp.context():
        # When
        response = client.get(path=HEALTH_CHECK_ENDPOINT)

        # Then
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert "unhealthy" in response.data["status"]
