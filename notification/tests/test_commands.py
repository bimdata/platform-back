import json
from unittest import mock

from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask

from notification.models import NotificationHistory
from notification.models import Project
from notification.models import Subscription


class ProjectNotificationEmailTest(TestCase):
    @mock.patch("externals.keycloak.get_access_token", return_value="123")
    def setUp(self, token_mock):
        super().setUp()
        self.project = Project.objects.create(api_id=100, cloud_id=100, name="Super Project")
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
        with mock.patch(
            "bimdata_api_client.api.webhook_api.WebhookApi.create_project_web_hook",
            side_effect=[{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}],
        ):
            Subscription.objects.create(
                project=self.project,
                document_creation=True,
                folder_creation=True,
                periodic_task=self.periodic_task,
                recipients_group_ids=[1, 2],
            )

    @mock.patch("externals.keycloak.get_access_token", return_value="123")
    def test_send_notification_email(self, token_mock):
        NotificationHistory.objects.create(
            project=self.project,
            event="document.creation",
            payload={
                "document": {
                    "history_count": 0,
                    "name": "my_doc.txt",
                    "created_at": "2025-07-01T12:08:49.951913Z",
                }
            },
        )

        with mock.patch(
            "bimdata_api_client.api.collaboration_api.CollaborationApi.get_project",
            return_value={"name": "Super Project"},
        ), mock.patch(
            "bimdata_api_client.api.collaboration_api.CollaborationApi.get_manage_group",
            return_value=mock.MagicMock(
                members=[
                    mock.MagicMock(email="test@bimdata.io", firstname="John", lastname="Doe")
                ]
            ),
        ):
            call_command("send_notification_email", self.project.api_id)

        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Activité du projet Super Project"

    @mock.patch(
        "bimdata_api_client.api.collaboration_api.CollaborationApi.get_project",
        return_value={"name": "Super Project"},
    )
    def test_send_notification_email_no_content(self, api_mock):
        call_command("send_notification_email", self.project.api_id)

        assert len(mail.outbox) == 0
