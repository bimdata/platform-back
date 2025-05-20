# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from rest_framework.test import APITestCase

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
            "recipients_group_id",
            "locale",
            "referer",
        }
        for field_name in subscription_model_field_names:
            if field_name not in non_subscription_fields:
                assert field_name in all_available_subscriptions
