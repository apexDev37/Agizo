"""URLs for the `orders` app.

URL and routing config for views defined in `orders`.
"""

from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path(
        "v1/orders/",
        views.create_order,
        name="create_order",
    ),
]
