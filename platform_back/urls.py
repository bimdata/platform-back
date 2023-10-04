# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
"""platform_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from organization import views as organization_views
from user import views as user_views
from webhooks import views as webhook_views

app_name = "platform_back"

router = DefaultRouter()

router.register(r"guidedtour", user_views.GuidedTourViewSet, basename="tours")
router.register(r"fav/clouds", user_views.FavoriteCloudViewSet, basename="fav-clouds")
router.register(r"fav/projects", user_views.FavoriteProjectViewSet, basename="fav-projects")

urlpatterns = [
    path(
        "create_or_update_user/",
        user_views.create_or_update_user,
        name="create_or_update_user",
    ),
    path(
        "create-cloud/",
        organization_views.create_cloud,
        name="create_cloud",
    ),
    path(
        "register-cloud/",
        organization_views.register_cloud,
        name="register_cloud",
    ),
    path("fav/", user_views.get_user_favorites, name="fav"),
    path("v1/", include("platform_back.v1.urls", namespace="v1")),
    path("webhook", webhook_views.WebHookView.as_view(), name="webhook_handler"),
    path("health/", include("health_check.urls")),
    path("", include(router.urls)),
]

if settings.ADMIN_INTERFACE:
    from django.contrib import admin
    from admin.views import register_webhooks_view

    urlpatterns += [
        path("grappelli/", include("grappelli.urls")),
        path(
            "admin/register-webhooks/",
            register_webhooks_view,
            name="webhooks_register_missing",
        ),
        path("admin/", admin.site.urls, name="admin"),
        path("admin/doc/", include("django.contrib.admindocs.urls")),
    ]

if "development" in settings.ENV:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
