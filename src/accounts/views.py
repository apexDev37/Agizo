"""Views for the `accounts` app.

DRF-based views to handle client requests to REST API endpoints.

For more details about this module
See: https://www.django-rest-framework.org/api-guide/views/
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.profiles import CustomerProfile
from accounts.serializers import CreateCustomerSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def create_customer(request: Request) -> Response:
    """Create and save a `User` and `CustomerProfile` instance."""
    serializer = CreateCustomerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    customer: CustomerProfile = serializer.save()
    return Response(
        status=status.HTTP_201_CREATED,
        data={
            "status": "success",
            "desc": "create user and customer profile.",
            "customer": {"name": customer.name, "email": customer.user.email},
        },
    )
