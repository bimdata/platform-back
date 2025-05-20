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
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from notification import views as notification_views
from organization import views as organization_views
from user import views as user_views
from webhooks import views as webhook_views

app_name = "platform_back_api"


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
    path("webhook", webhook_views.WebHookView.as_view(), name="webhook_handler"),
    path(
        "cloud/<int:cloud_id>/project/<int:project_id>/notification",
        notification_views.NotificationView.as_view(),
        name="notifications",
    ),
    path(
        "notification/webhook",
        notification_views.webhook,
        name="notifications-webhook",
    ),
    path("", include(router.urls)),
]
