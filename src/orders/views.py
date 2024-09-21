"""Views for the `orders` app.

DRF-based views to handle client requests to REST API endpoints.

For more details about this module
See: https://www.django-rest-framework.org/api-guide/views/
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from orders.serializers import CreateOrderSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def create_order(request: Request) -> Response:
    """Create and save an `Order` instance made by a customer user."""
    serializer = CreateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    order = serializer.save()
    return Response(
        status=status.HTTP_201_CREATED,
        data={
            "status": "success",
            "desc": "create order for customer user",
            "order": {
                "id": order.id,
                "created_at": order.created_at,
                "customer": {"phone_number": order.customer.phone_number},
            },
        },
    )
