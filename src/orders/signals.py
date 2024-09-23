"""Signals for the `orders` app.

Define custom signals and handlers.
"""

from collections.abc import MutableMapping
from typing import Any

from django.dispatch import Signal, receiver

from accounts.profiles import CustomerProfile
from orders.models import Order
from orders.serializers import CreateOrderSerializer
from orders.services import OrdersSMSService
from orders.utils import init_africastalking_sms_service

# Custom signal to repr order created.
post_create_order = Signal()


@receiver(post_create_order, sender=CreateOrderSerializer)
def notify_customer(
    sender: type[Any],
    order: Order,
    customer: CustomerProfile,
    **kwargs: MutableMapping[str, Any],
) -> None:
    """Handler to send SMS notification to the customer on created order."""
    sms_client = init_africastalking_sms_service()
    service = OrdersSMSService(client=sms_client)
    service.notify_customer(customer)
