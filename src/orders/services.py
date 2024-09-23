"""Services for the `orders` app.

Abstractions responsible to execute key app functionalities and use cases.
"""

from africastalking.SMS import SMSService
from requests import Response  # type: ignore[import-untyped]

from accounts.profiles import CustomerProfile


class OrdersSMSService:
    """Service responsible to notify customers on created orders.

    This class primarily acts as a wrapper to create boundaries between our app
    and the 3rd-party vendor's SDK.

    Note:
        - Currently this service only supports injecting a `client` of type
        `africastalking.SMS.SMSService` to serve SMS notifications.
        - The sender ID is alphanumeric; this means only messages can be sent
        one way, to a customer but not received.
    """

    _message: str = "Hello {name}, your order has been received and processed."
    _sender_id: str = "Agizo"

    def __init__(  # noqa: D107
        self, client: SMSService, sender: str = _sender_id
    ) -> None:
        if not isinstance(client, SMSService):
            errmsg = "client must be of type `africastalking.SMS.SMSService`"
            raise TypeError(errmsg)
        self.client = client
        self.sender = sender

    def notify_customer(
        self, customer: CustomerProfile, msg: str = _message
    ) -> Response:
        """Wrapper method to notify customer on created order via SMS."""
        response = self.client.send(
            message=msg.format(name=customer.name),
            recipients=[customer.phone_number],
            sender_id=self.sender,
        )
        return response
