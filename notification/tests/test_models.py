# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from datetime import datetime

from rest_framework.test import APITestCase

from notification.models import NotificationHistory
from notification.models import Project
from notification.models import Subscription
from notification.models import subscription_to_webhook_event


class SubscriptionModelTest(APITestCase):
    def test_all_available_subscriptions_are_defined_in_model(self):
        all_available_subscriptions = subscription_to_webhook_event.keys()

        subscription_model_field_names = {
            field.name for field in Subscription._meta.get_fields(include_parents=False)
        }
        for subscription_name in all_available_subscriptions:
            assert subscription_name in subscription_model_field_names

        non_subscription_fields = {
            "id",
            "project",
            "periodic_task",
            "recipients_group_ids",
            "locale",
            "referer",
        }
        for field_name in subscription_model_field_names:
            if field_name not in non_subscription_fields:
                assert field_name in all_available_subscriptions


class NotificationHistoryModelTest(APITestCase):
    def test_all_available_subscriptions_are_defined_in_model(self):
        project = Project.objects.create(api_id=100, cloud_id=100, name="Super Project")

        notif = NotificationHistory.objects.create(
            project=project,
            event="document.creation",
            payload={
                "document": {
                    "history_count": 0,
                    "name": "my_doc.txt",
                    "created_at": "2025-07-01T12:08:49.951913Z",
                }
            },
        )
        print(notif.parsed_payload)
        print(type(notif.parsed_payload["document"]["created_at"]))
        assert isinstance(notif.parsed_payload["document"]["created_at"], datetime)
