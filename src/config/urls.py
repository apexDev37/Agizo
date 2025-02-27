"""URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path

import accounts
import accounts.views
import config
import config.views
from config.constants import ENABLE_DEBUG_TOOLBAR

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.urls", namespace="accounts")),
    path("api/", include("orders.urls", namespace="orders")),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("", accounts.views.home_view, name="home"),
    path("meta/health/", config.views.health_check, name="health_check"),
]

if ENABLE_DEBUG_TOOLBAR:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns.extend(debug_toolbar_urls())
