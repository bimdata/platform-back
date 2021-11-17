from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("", admin.site.urls, name="admin"),
    path("doc/", include("django.contrib.admindocs.urls")),
]

if "development" in settings.ENV:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
