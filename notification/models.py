from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

from externals import keycloak
from externals.bimdata_api import ApiClient


subscription_to_webhook_event = {
    "document_creation": "document.creation",
    "document_deletion": "document.deletion",
    "folder_creation": "folder.creation",
    "folder_deletion": "folder.deletion",
    "visa_creation": "visa.creation",
    "visa_deletion": "visa.deletion",
    "visa_validation": "visa.validation.add",
    "visa_denied": "visa.validation.denied",
    "bcf_topic_creation": "bcf.topic.creation",
    "bcf_topic_deletion": "bcf.topic.deletion",
    "invitation_accepted": "project.invitation.accepted",
    "model_creation": "model.creation",
    "model_deletion": "model.deletion",
}

# assert no duplication. If two subscription have the same event, remove one subcription will disable the webhook for other events too
assert len(subscription_to_webhook_event.values()) == len(
    set(subscription_to_webhook_event.values())
), "Webhook events can't be duplicated"

webhook_event_to_subcription = {
    event: subscription for subscription, event in subscription_to_webhook_event.items()
}


class Project(models.Model):
    api_id = models.PositiveIntegerField(unique=True)
    cloud_id = models.PositiveIntegerField()
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name} ({self.api_id})"


class Subscription(models.Model):
    project = models.OneToOneField("Project", on_delete=models.CASCADE)
    periodic_task = models.OneToOneField(
        "django_celery_beat.PeriodicTask", on_delete=models.CASCADE
    )

    recipients_group_id = models.PositiveIntegerField()

    LOCALE_FR = "fr"
    LOCALE_EN = "en"
    LOCALE_CHOICES = ((LOCALE_FR, "Français"), (LOCALE_EN, "English"))

    locale = models.CharField(max_length=2, choices=LOCALE_CHOICES, default=LOCALE_EN)

    referer = models.URLField(
        max_length=255, null=True, blank=True, default=settings.PLATFORM_URL
    )

    document_creation = models.BooleanField(default=False)
    document_deletion = models.BooleanField(default=False)
    folder_creation = models.BooleanField(default=False)
    folder_deletion = models.BooleanField(default=False)
    visa_creation = models.BooleanField(default=False)
    visa_deletion = models.BooleanField(default=False)
    visa_validation = models.BooleanField(default=False)
    visa_denied = models.BooleanField(default=False)
    bcf_topic_creation = models.BooleanField(default=False)
    bcf_topic_deletion = models.BooleanField(default=False)
    invitation_accepted = models.BooleanField(default=False)
    model_creation = models.BooleanField(default=False)
    model_deletion = models.BooleanField(default=False)

    def __str__(self):
        return f"Subscription for {self.project}"

    def update_webhooks(self):
        current_webhooks = NotificationWebhook.objects.filter(project=self.project)

        current_webhooks_by_event = {}

        for webhook in current_webhooks:
            current_webhooks_by_event[webhook.event] = webhook

        for subscription, event in subscription_to_webhook_event.items():
            if getattr(self, subscription) is True and event not in current_webhooks_by_event:
                # Create all missing webhook
                NotificationWebhook.objects.create(project=self.project, event=event)

            if getattr(self, subscription) is False and event in current_webhooks_by_event:
                current_webhooks_by_event[event].unregister()


class NotificationHistory(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    event = models.CharField(max_length=255)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    consumed = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.project} with event {self.event}"


class NotificationWebhook(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    webhook_id = models.PositiveIntegerField(unique=True, help_text="Webhook id from API")
    secret = models.CharField(max_length=256)
    event = models.CharField(max_length=256)

    class Meta:
        unique_together = (("project", "event"),)

    def __str__(self):
        return f"Webhook for {self.project} with event {self.event}"

    def save(self, *args, **kwargs):
        client = ApiClient(keycloak.get_access_token())
        secret = get_random_string(64)

        api_webhook = client.webhook_api.create_project_web_hook(
            cloud_pk=self.project.cloud_id,
            project_pk=self.project.api_id,
            web_hook_request={
                "events": [self.event],
                "url": settings.PLATFORM_BACK_URL + reverse("v1:notifications-webhook"),
                "secret": secret,
            },
        )
        self.secret = secret
        self.webhook_id = api_webhook["id"]
        return super().save(*args, **kwargs)

    def unregister(self):
        client = ApiClient(keycloak.get_access_token())
        client.webhook_api.delete_project_web_hook(
            cloud_pk=self.project.cloud_id,
            project_pk=self.project.api_id,
            id=self.webhook_id,
        )
        self.delete()
