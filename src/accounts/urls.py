"""URLs for the `accounts` app.

URL and routing config for views defined in `accounts`.
"""

from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path(
        "v1/customers/",
        views.create_customer,
        name="create_customer",
    ),
]
