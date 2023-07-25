from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

from admin.views import register_webhooks

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("", admin.site.urls, name="admin"),
    path(
        "admin/register-webhooks/",
        register_webhooks,
        name="webhooks_register_missing",
    ),
    path("doc/", include("django.contrib.admindocs.urls")),
]

if "development" in settings.ENV:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
