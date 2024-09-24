"""Managers for the `accounts` app.

Define managers for models registered under `accounts`.

Note:
    - The `profiles` module defines models related to user profiles.
"""

from collections.abc import MutableMapping
from typing import Any

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

IS_ACTIVE: str = "is_active"
IS_STAFF: str = "is_staff"
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
        extra_fields.setdefault(IS_STAFF, True)

        if extra_fields.get(IS_SUPERUSER) is not True:
            errmsg = f"Superuser must have {IS_SUPERUSER}=True."
            raise ValueError(errmsg)
        return self.create_user(email, password, **extra_fields)
