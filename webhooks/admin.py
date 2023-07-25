from django.contrib import admin

from webhooks.models import WebHook


@admin.register(WebHook)
class WebHookAdmin(admin.ModelAdmin):
    change_list_template = "admin/webhook_change_list.html"
    list_display = ("webhook_id", "cloud_id", "created_at")
    readonly_fields = ("webhook_id", "cloud_id", "created_at")
