"""Serializer tests for the `accounts` app.

Define serializers to support data validation and serialization/deserialization
for the `accounts.models`.

For more details about this file
See: https://www.django-rest-framework.org/api-guide/serializers/
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.profiles import CustomerProfile
from accounts.serializers import CreateCustomerSerializer

User = get_user_model()


@pytest.mark.unit()
def test_should_raise_validation_error_on_invalid_user_data() -> None:
    # Given
    invalid = {
        "name": "John Doe",
        "phone_number": "+245000000000",
        "user_email": "nonexistent",
        "user_password": "tooshort",
    }

    with pytest.raises(serializers.ValidationError, match=""):  # Then
        _ = CreateCustomerSerializer(data=invalid).is_valid(
            raise_exception=True
        )  # When


@pytest.mark.unit()
def test_should_raise_validation_error_on_invalid_customer_data() -> None:
    # Given
    invalid = {
        "name": "",
        "phone_number": "123",
        "user_email": "johndoe@email.example",
        "user_password": "jd-secret-pwd",
    }

    with pytest.raises(serializers.ValidationError, match=""):  # Then
        _ = CreateCustomerSerializer(data=invalid).is_valid(
            raise_exception=True
        )  # When


@pytest.mark.unit()
def test_should_accept_valid_serializer_user_and_customer_client_data() -> None:
    # Given
    valid = {
        "name": "John Doe",
        "phone_number": "+245000000000",
        "user_email": "johndoe@email.example",
        "user_password": "jd-secret-pwd",
    }

    # When
    serializer = CreateCustomerSerializer(data=valid)

    # Then
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db()
def test_should_persist_valid_user_and_customer_models_in_serializer() -> None:
    # Given
    valid = {
        "name": "John Doe",
        "phone_number": "+245000000000",
        "user_email": "johndoe@email.example",
        "user_password": "jd-secret-pwd",
    }
    serializer = CreateCustomerSerializer(data=valid)

    # When
    assert serializer.is_valid(), serializer.errors
    customer = serializer.save()

    # Then
    assert isinstance(customer, CustomerProfile)
    assert User.objects.filter(email=valid["user_email"]).exists()
    assert CustomerProfile.objects.filter(phone_number=valid["phone_number"]).exists()
