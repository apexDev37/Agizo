"""Backend module for OIDC lib.

This module defines a custom backend that inherits from
`mozilla_django_oidc.auth.OIDCAuthenticationBackend` to override methods to meet
the project-specific requirements and use cases.

For examples on overrides and custom backends
See: https://mozilla-django-oidc.readthedocs.io/en/stable/installation.html
"""

import secrets

from django.contrib.auth.models import AbstractBaseUser
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CustomOIDCAuthBackend(OIDCAuthenticationBackend):
    """Custom OIDC auth backend for Django project.

    @TODO(apexDev37)
    Consider overriding `update_user` for new or changed user claims.
    """

    def create_user(self, claims: dict[str, str]) -> AbstractBaseUser:
        """Return object for a newly created custom auth user.

        Note:
            - Optionally extract additional claims from ID token and assign
            then to your `User` model before save.
            - This method generates a placeholder password for the OIDC user
            which is a system requirement. Given authentication occurs with
            an OP (Google), the local password is not required to authenticate.
            - Change the User field `is_active` to `True` for OIDC-authenticated
            users to enable them to login.
        """
        email = claims.get("email")
        if not email:
            errmsg = "OIDC token does not contain required `email` claim"
            raise ValueError(errmsg)

        user = self.UserModel.objects.create_user(
            email=email, password=secrets.token_urlsafe()
        )

        user.is_active = True
        user.save(update_fields=["is_active"])
        return user
