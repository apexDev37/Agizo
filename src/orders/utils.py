"""Utility module for the `orders` app.

Utils to provide functions required to support the `orders` Django app.
This consists of getters, helpers, and more at a app-level.

Note:
    - Consider moving your utility to the project level if used across
    various apps or is highly contextual to the Django project.
"""

import africastalking
from africastalking.SMS import SMSService
from django.conf import settings


def init_africastalking_sms_service() -> SMSService:
    """Return initialized and configured SMS service ready to use."""
    africastalking.initialize(
        username=settings.AFRICAS_TALKING_USERNAME,
        api_key=settings.AFRICAS_TALKING_API_KEY,
    )
    return africastalking.SMS
