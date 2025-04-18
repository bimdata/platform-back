# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import json
from unittest import mock

from django.urls import reverse
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask
from rest_framework import status
from rest_framework.test import APITestCase

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

    @mock.patch.object(IsProjectAdmin, "has_permission")
    def test_update_with_new(self, permission_mock):
        permission_mock.return_value = True
        url = reverse("update-notifications", kwargs={"cloud_id": 99, "project_id": 99})

        body = {
            "file_creation": True,
            "file_deletion": True,
            "file_new_version": True,
            "file_new_version": True,
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

        assert subscription.file_creation is True
        assert subscription.file_deletion is True
        assert subscription.file_new_version is True
        assert subscription.folder_creation is False
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

    @mock.patch.object(IsProjectAdmin, "has_permission")
    def test_update_with_existing(self, permission_mock):
        permission_mock.return_value = True
        url = reverse("update-notifications", kwargs={"cloud_id": 100, "project_id": 100})

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
            file_creation=True,
            file_new_version=True,
            periodic_task=periodic_task,
        )

        body = {
            "file_creation": False,
            "file_deletion": True,
            "file_new_version": True,
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
        assert subscription.file_creation is False
        assert subscription.file_deletion is True
        assert subscription.file_new_version is True
        assert subscription.folder_creation is False
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
