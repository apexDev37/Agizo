"""Profiles for the `accounts` app.

Profiles are a pattern to extend the custom auth user model to decouple
concerns and independently scale diverse user representations.
Define custom user profiles in this dedicated module, `profiles.py`.

Note:
    - `profiles` is not an official Django module naming convention.
"""

from django.conf import settings
from django.db import models


class CustomerProfile(models.Model):
    """Custom user profile to represent a `customer` entity."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(
        blank=False,
        null=False,
        max_length=50,
    )
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)

    class Meta:
        """Optional model metadata."""

        db_table = "accounts_customer_profiles"
        verbose_name = "customer"
        verbose_name_plural = "customers"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"<Customer {self.id}: email: {self.user.email} name: ({self.name})>"
