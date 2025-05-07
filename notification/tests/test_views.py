# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import hashlib
import hmac
import json
from unittest import mock

from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask
from rest_framework import status
from rest_framework.test import APITestCase

from notification.models import NotificationHistory
from notification.models import NotificationWebhook
from notification.models import Project
from notification.models import Subscription
from notification.permissions import IsProjectAdmin
from user.models import User


class NotificationViewTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(
            username="John Doe", first_name="John", last_name="Doe"
        )
        self.client.force_authenticate(user=self.user, token="don't care for now")

    @mock.patch(
        "bimdata_api_client.api.webhook_api.WebhookApi.create_project_web_hook",
        side_effect=[{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}],
    )
    @mock.patch("externals.keycloak.get_access_token")
    @mock.patch.object(IsProjectAdmin, "has_permission", return_value=True)
    def test_update_with_new(self, permission_mock, token_mock, api_mock):
        url = reverse("v1:notifications", kwargs={"cloud_id": 99, "project_id": 99})

        body = {
            "recipients_group_id": 1,
            "document_creation": True,
            "document_deletion": True,
            "folder_creation": True,
            "folder_deletion": False,
            "schedule": {
                "time": "09:30",
                "timezone": "Europe/Paris",
                "monday": True,
                "tuesday": False,
                "wednesday": False,
                "thursday": True,
                "friday": False,
                "saturday": False,
                "sunday": False,
            },
        }

        response = self.client.put(url, data=body)

        assert response.status_code == status.HTTP_200_OK

        subscription = Subscription.objects.get(project__api_id=99)

        assert subscription.document_creation is True
        assert subscription.document_deletion is True
        assert subscription.folder_creation is True
        assert subscription.folder_deletion is False
        assert subscription.periodic_task.name == "Notification schedule for project 99"
        assert (
            subscription.periodic_task.task
            == "platform_back.tasks.notifications.send_project_notifications_email"
        )
        assert json.loads(subscription.periodic_task.kwargs)["project_id"] == 99
        assert subscription.periodic_task.crontab.hour == "09"
        assert subscription.periodic_task.crontab.minute == "30"
        assert str(subscription.periodic_task.crontab.timezone) == "Europe/Paris"
        assert subscription.periodic_task.crontab.day_of_week == "1,4"

    @mock.patch(
        "bimdata_api_client.api.webhook_api.WebhookApi.create_project_web_hook",
        side_effect=[{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}],
    )
    @mock.patch("externals.keycloak.get_access_token")
    @mock.patch.object(IsProjectAdmin, "has_permission", return_value=True)
    def test_update_with_existing(self, permission_mock, token_mock, api_mock):
        url = reverse("v1:notifications", kwargs={"cloud_id": 100, "project_id": 100})

        project = Project.objects.create(api_id=100, cloud_id=100)
        crontab = CrontabSchedule.objects.create(
            minute="00",
            hour="19",
            timezone="Europe/Paris",
            day_of_week="1,2,5",
        )
        periodic_task = PeriodicTask.objects.create(
            crontab=crontab,
            name="Notification schedule for project 100",
            task="platform_back.tasks.notifications.send_project_notifications_email",
            kwargs=json.dumps(
                {
                    "project_id": 100,
                }
            ),
        )
        subscription = Subscription.objects.create(
            project=project,
            document_creation=True,
            folder_creation=True,
            periodic_task=periodic_task,
            recipients_group_id=1,
        )

        body = {
            "recipients_group_id": 2,
            "document_creation": False,
            "document_deletion": True,
            "folder_creation": True,
            "schedule": {
                "time": "19:45",
                "timezone": "Europe/London",
                "monday": True,
                "tuesday": False,
                "wednesday": True,
                "thursday": False,
                "friday": False,
                "saturday": True,
                "sunday": True,
            },
        }

        response = self.client.put(url, data=body)

        assert response.status_code == status.HTTP_200_OK

        subscription.refresh_from_db()
        assert subscription.recipients_group_id == 2
        assert subscription.document_creation is False
        assert subscription.document_deletion is True
        assert subscription.folder_creation is True
        assert subscription.folder_deletion is False
        assert subscription.periodic_task.name == "Notification schedule for project 100"
        assert (
            subscription.periodic_task.task
            == "platform_back.tasks.notifications.send_project_notifications_email"
        )
        assert json.loads(subscription.periodic_task.kwargs)["project_id"] == 100
        assert subscription.periodic_task.crontab.hour == "19"
        assert subscription.periodic_task.crontab.minute == "45"
        assert str(subscription.periodic_task.crontab.timezone) == "Europe/London"
        assert subscription.periodic_task.crontab.day_of_week == "1,3,6,7"

    @mock.patch(
        "bimdata_api_client.api.webhook_api.WebhookApi.create_project_web_hook",
        side_effect=[{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}],
    )
    @mock.patch("externals.keycloak.get_access_token")
    @mock.patch.object(IsProjectAdmin, "has_permission", return_value=True)
    def test_get_notifications(self, permission_mock, token_mock, api_mock):
        url = reverse("v1:notifications", kwargs={"cloud_id": 100, "project_id": 100})

        project = Project.objects.create(api_id=100, cloud_id=100)
        crontab = CrontabSchedule.objects.create(
            minute="00",
            hour="19",
            timezone="Europe/Paris",
            day_of_week="1,2,5",
        )
        periodic_task = PeriodicTask.objects.create(
            crontab=crontab,
            name="Notification schedule for project 100",
            task="platform_back.tasks.notifications.send_project_notifications_email",
            kwargs=json.dumps(
                {
                    "project_id": 100,
                }
            ),
        )
        subscription = Subscription.objects.create(
            project=project,
            document_creation=True,
            folder_creation=True,
            periodic_task=periodic_task,
            recipients_group_id=1,
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == subscription.id

    @mock.patch(
        "bimdata_api_client.api.webhook_api.WebhookApi.create_project_web_hook",
        side_effect=[{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}],
    )
    @mock.patch("externals.keycloak.get_access_token")
    @mock.patch("notification.models.NotificationWebhook.unregister")
    @mock.patch.object(IsProjectAdmin, "has_permission", return_value=True)
    def test_delete_notifications(
        self, permission_mock, unregister_mock, token_mock, api_mock
    ):
        url = reverse("v1:notifications", kwargs={"cloud_id": 100, "project_id": 100})

        project = Project.objects.create(api_id=100, cloud_id=100)
        crontab = CrontabSchedule.objects.create(
            minute="00",
            hour="19",
            timezone="Europe/Paris",
            day_of_week="1,2,5",
        )
        periodic_task = PeriodicTask.objects.create(
            crontab=crontab,
            name="Notification schedule for project 100",
            task="platform_back.tasks.notifications.send_project_notifications_email",
            kwargs=json.dumps(
                {
                    "project_id": 100,
                }
            ),
        )
        subscription = Subscription.objects.create(
            project=project,
            document_creation=True,
            folder_creation=True,
            periodic_task=periodic_task,
            recipients_group_id=1,
        )
        subscription.update_webhooks()
        assert NotificationWebhook.objects.filter(project=project).exists()

        NotificationHistory.objects.create(
            project=project,
            event="document.creation",
            payload={},
        )

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Subscription.objects.filter(id=subscription.id).exists()
        assert not PeriodicTask.objects.filter(id=periodic_task.id).exists()
        assert not NotificationWebhook.objects.filter(project=project).exists()
        assert unregister_mock.called
        assert not NotificationHistory.objects.filter(project=project).exists()


class NotificationWebhookViewTest(APITestCase):
    @mock.patch(
        "bimdata_api_client.api.webhook_api.WebhookApi.create_project_web_hook",
        side_effect=[{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}],
    )
    @mock.patch("externals.keycloak.get_access_token")
    def setUp(self, token_mock, api_mock):
        super().setUp()
        self.cloud_id = 100
        self.project = Project.objects.create(api_id=100, cloud_id=self.cloud_id)
        self.crontab = CrontabSchedule.objects.create(
            minute="00",
            hour="19",
            timezone="Europe/Paris",
            day_of_week="1,2,5",
        )
        self.periodic_task = PeriodicTask.objects.create(
            crontab=self.crontab,
            name="Notification schedule for project 100",
            task="platform_back.tasks.notifications.send_project_notifications_email",
            kwargs=json.dumps(
                {
                    "project_id": 100,
                }
            ),
        )
        self.subscription = Subscription.objects.create(
            project=self.project,
            document_creation=True,
            folder_creation=True,
            periodic_task=self.periodic_task,
            recipients_group_id=1,
        )

        self.subscription.update_webhooks()
        self.event = "document.creation"
        self.webhook = NotificationWebhook.objects.get(event=self.event)

    def test_send_with_no_signature(self):
        url = reverse("v1:notifications-webhook")

        body = {"some": "data"}

        response = self.client.post(url, data=body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"x-bimdata-signature": "Header required"}

    def test_send_with_invalid_signature(self):
        url = reverse("v1:notifications-webhook")

        body = {
            "event_name": self.event,
            "webhook_id": self.webhook.webhook_id,
            "cloud_id": self.cloud_id,
            "project_id": self.project.api_id,
            "data": {"some": "data"},
        }
        str_payload = json.dumps(body, cls=DjangoJSONEncoder).encode()
        signature = hmac.new(
            "super invalid secret".encode(), str_payload, hashlib.sha256
        ).hexdigest()

        response = self.client.post(
            url,
            data=body,
            headers={"Content-Type": "application/json", "x-bimdata-signature": signature},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"x-bimdata-signature": "Bad request signature"}

    def test_cloud_id_changed_when_project_id_is_moved(self):
        url = reverse("v1:notifications-webhook")
        event = "document.creation"

        body = {
            "event_name": event,
            "webhook_id": self.webhook.webhook_id,
            "cloud_id": 999,
            "project_id": self.project.api_id,
            "data": {"some": "data"},
        }
        str_payload = json.dumps(body, cls=DjangoJSONEncoder, separators=(",", ":")).encode()
        signature = hmac.new(
            self.webhook.secret.encode(), str_payload, hashlib.sha256
        ).hexdigest()

        response = self.client.post(
            url, data=body, format="json", headers={"x-bimdata-signature": signature}
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert Project.objects.filter(api_id=self.project.api_id, cloud_id=999).exists()

    def test_send_with_valid_signature(self):
        url = reverse("v1:notifications-webhook")
        event = "document.creation"

        body = {
            "event_name": event,
            "webhook_id": self.webhook.webhook_id,
            "cloud_id": self.cloud_id,
            "project_id": self.project.api_id,
            "data": {"some": "data"},
        }
        str_payload = json.dumps(body, cls=DjangoJSONEncoder, separators=(",", ":")).encode()
        signature = hmac.new(
            self.webhook.secret.encode(), str_payload, hashlib.sha256
        ).hexdigest()

        response = self.client.post(
            url, data=body, format="json", headers={"x-bimdata-signature": signature}
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_send_with_valid_signature_and_incomplete_data(self):
        url = reverse("v1:notifications-webhook")
        event = "document.creation"

        body = {
            "event_name": event,
            "cloud_id": self.cloud_id,
            "project_id": self.project.api_id,
            "data": {"some": "data"},
        }
        str_payload = json.dumps(body, cls=DjangoJSONEncoder, separators=(",", ":")).encode()
        signature = hmac.new(
            self.webhook.secret.encode(), str_payload, hashlib.sha256
        ).hexdigest()

        response = self.client.post(
            url, data=body, format="json", headers={"x-bimdata-signature": signature}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_send_with_valid_signature_and_unknown_webhook(self):
        url = reverse("v1:notifications-webhook")
        event = "document.creation"

        body = {
            "event_name": event,
            "webhook_id": 999,
            "cloud_id": self.cloud_id,
            "project_id": self.project.api_id,
            "data": {"some": "data"},
        }
        str_payload = json.dumps(body, cls=DjangoJSONEncoder, separators=(",", ":")).encode()
        signature = hmac.new(
            self.webhook.secret.encode(), str_payload, hashlib.sha256
        ).hexdigest()

        response = self.client.post(
            url, data=body, format="json", headers={"x-bimdata-signature": signature}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_send_with_invalid_signature_and_unknown_webhook(self):
        url = reverse("v1:notifications-webhook")
        event = "document.creation"

        body = {
            "event_name": event,
            "webhook_id": 999,
            "cloud_id": self.cloud_id,
            "project_id": self.project.api_id,
            "data": {"some": "data"},
        }

        response = self.client.post(
            url, data=body, format="json", headers={"x-bimdata-signature": "123"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
