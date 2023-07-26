# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, GuidedTour
from user.models import Notification


@admin.register(User)
class UsersAdmin(UserAdmin):
    fieldsets = (
        ("platform_info", {"fields": ("demo_cloud", "demo_project", "sub")}),
    ) + UserAdmin.fieldsets
    list_display = ("username", "email", "first_name", "last_name", "date_joined")
    list_filter = ("is_superuser",)
    ordering = ("-date_joined",)


@admin.register(GuidedTour)
class GuidedTourAdmin(admin.ModelAdmin):
    list_display = ("user", "name")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "cloud_id", "event", "event_type", "consumed", "created_at")
    list_filter = (
        "event_type",
        "event",
    )
    ordering = ("-created_at",)
