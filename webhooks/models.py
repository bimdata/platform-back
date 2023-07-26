from django.db import models


class WebHook(models.Model):
    webhook_id = models.PositiveIntegerField(
        unique=True, help_text="Webhook id from API"
    )
    cloud_id = models.PositiveIntegerField()
    secret = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
