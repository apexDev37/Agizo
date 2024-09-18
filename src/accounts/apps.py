"""App module for the `accounts` app.

Entry-point for Django app introspection and metadata configuration.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for the `accounts` Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
