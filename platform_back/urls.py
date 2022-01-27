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
from django.urls import path, include
from user import views
from webhooks.views import WebHookHandler

app_name = "platform_back"

urlpatterns = [
    path(
        "create_or_update_user/",
        views.create_or_update_user,
        name="create_or_update_user",
    ),
    path("v1/", include("platform_back.v1.urls", namespace="v1")),
    path("webhook", WebHookHandler.as_view(), name="webhook-handler"),
    path("health/", include("health_check.urls")),
]

if settings.ADMIN_INTERFACE:
    from django.contrib import admin

    urlpatterns += [
        path("grappelli/", include("grappelli.urls")),
        path("admin/", admin.site.urls, name="admin"),
        path("admin/doc/", include("django.contrib.admindocs.urls")),
    ]

if "development" in settings.ENV:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
