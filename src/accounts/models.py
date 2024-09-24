"""Models for the `accounts` app.

Define models and managers registered under `accounts`.
Managers can optionally be defined in a dedicated module, `managers.py`.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts.managers import UserManager
from accounts.profiles import CustomerProfile  # noqa: F401


class User(AbstractBaseUser, PermissionsMixin):
    """Custom auth user model.

    Inherit from `AbstractBaseUser` to define a model from scratch.
    """

    email = models.EmailField(max_length=254, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Required boolean fields for Django Admin compatibility.
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        """Optional model metadata."""

        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<User {self.id}: email: {self.email}, active: {self.is_active}>"
