"""Models for the `accounts` app.

Define models and managers registered under `accounts`.
Managers can optionally be defined in a dedicated module, `managers.py`.
"""

from collections.abc import MutableMapping
from typing import Any

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

IS_ACTIVE: str = "is_active"
IS_SUPERUSER: str = "is_superuser"


class UserManager(BaseUserManager):
    """Custom user model manager.

    Manager required when implementing custom user model.

    Note:
        - `create_user` and `create_superuser` methods must be defined.
    """

    def create_user(
        self, email: str, password: str, **extra_fields: MutableMapping[str, Any]
    ) -> AbstractBaseUser:
        """Defines fields to create and save user instances."""
        if not email:
            errmsg = "User must have an email"
            raise ValueError(errmsg)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str, **extra_fields: MutableMapping[str, Any]
    ) -> AbstractBaseUser:
        """Defines fields to create and save superuser instances."""
        extra_fields.setdefault(IS_SUPERUSER, True)
        extra_fields.setdefault(IS_ACTIVE, True)

        if extra_fields.get(IS_SUPERUSER) is not True:
            errmsg = f"Superuser must have {IS_SUPERUSER}=True."
            raise ValueError(errmsg)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """Custom auth user model.

    Inherit from `AbstractBaseUser` to define a model from scratch.
    """

    email = models.EmailField(max_length=254, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        """Optional model metadata."""

        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<User {self.id}: email: {self.email}, active: {self.is_active}>"


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
