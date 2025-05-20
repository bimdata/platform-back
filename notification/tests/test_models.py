# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import json

from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask
from rest_framework.test import APITestCase

from notification.models import Project
from notification.models import Subscription
from notification.models import subscription_to_webhook_event


class SubscriptionModelTest(APITestCase):
    def test_all_available_are_defined_in_model(self):
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
            periodic_task=periodic_task,
            recipients_group_id=1,
        )
        all_available_subscriptions = subscription_to_webhook_event.keys()
        for subscription_name in all_available_subscriptions:
            assert hasattr(subscription, subscription_name)

        non_subscription_fields = {
            "id",
            "project",
            "periodic_task",
            "recipients_group_id",
            "locale",
            "referer",
        }
        for field in Subscription._meta.get_fields(include_parents=False):
            if field.name not in non_subscription_fields:
                assert field.name in all_available_subscriptions
