from django.contrib import admin

from notification.models import NotificationHistory
from notification.models import NotificationWebhook
from notification.models import Project
from notification.models import Subscription


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("api_id", "cloud_id", "name")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("project",)
    raw_id_fields = ("project",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("project")
        return qs


@admin.register(NotificationWebhook)
class NotificationWebhookAdmin(admin.ModelAdmin):
    list_display = ("project", "event", "webhook_id")
    raw_id_fields = ("project",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("project")
        return qs


@admin.register(NotificationHistory)
class NotificationHistoryAdmin(admin.ModelAdmin):
    list_display = ("project", "event", "created_at", "consumed")
    raw_id_fields = ("project",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("project")
        return qs
