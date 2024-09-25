"""Serializers for the `accounts` app.

Define serializers to support data validation and serialization/deserialization
for the `accounts.models`.

For more details about this file
See: https://www.django-rest-framework.org/api-guide/serializers/
"""

from collections.abc import MutableMapping
from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.profiles import CustomerProfile

User = get_user_model()


class CreateCustomerSerializer(serializers.ModelSerializer):
    """Serializer to serialize/deserialize CustomerProfile instances.

    Note:
        - This serializer extracts user details from the request to retrieve the
        user `email` to form the required `User` to `CustomerProfile` relation.
        - By design, we don't allow the user to pass in an email. This prevents
        user A with an email {userA@email.com} from creating a `CustomerProfile`
        with another user's email {userB@email.com}.
    """

    name = serializers.CharField(allow_blank=False)
    phone_number = serializers.CharField(min_length=10)
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:  # noqa: D106
        model = CustomerProfile
        fields = (
            "name",
            "phone_number",
            "owner",
        )

    def create(self, validated_data: MutableMapping[str, Any]) -> CustomerProfile:
        request_user = validated_data.pop("owner")
        user = User.objects.filter(email=request_user.email).first()
        return CustomerProfile.objects.create(user=user, **validated_data)


# TODO(apexDev37): refactor
# Ideally, user related fields should be in a dedicated `UserSerializer`.
# Given the single use case to add `customers`, this is all we need.
# See: https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects


class CreateUserAndCustomerSerializer(serializers.ModelSerializer):
    """Serializer to serialize/deserialize CustomerProfile instances.

    Note:
        - This serializer is ideal for Admins who can have the ability to
        create both users and customers.
        - This serializer performs validation and DB persistence for
        two related models `User` and `CustomerProfile`.
    """

    name = serializers.CharField()
    phone_number = serializers.CharField(min_length=10)
    user_email = serializers.EmailField()
    user_password = serializers.CharField(min_length=9, write_only=True)

    class Meta:  # noqa: D106
        model = CustomerProfile
        fields = (
            "name",
            "phone_number",
            "user_email",
            "user_password",
        )
        read_only_fields = ("phone_number",)

    def create(self, validated_data: MutableMapping[str, Any]) -> CustomerProfile:
        email = validated_data.pop("user_email")
        password = validated_data.pop("user_password")
        user = User.objects.create_user(email=email, password=password)

        return CustomerProfile.objects.create(user=user, **validated_data)
