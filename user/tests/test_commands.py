from datetime import timedelta
from unittest.mock import MagicMock

from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APITestCase

from user.models import Notification, User


class UserNotificationTests(APITestCase):
    def setUp(self):
        self.request = MagicMock(method="GET")

        self.user = User.objects.create(
            username="John Doe",
            first_name="John",
            last_name="Doe",
            language="fr",
            email="john.doe@domain.tld",
        )

        self.notif = Notification.objects.create(
            user=self.user,
            cloud_id="1",
            event="add",
            event_type="visa",
            payload={},
        )

        self.notif.created_at = timezone.now() - timedelta(minutes=10)
        self.notif.save()
        self.notif.refresh_from_db()

    def test_notify_users_command(self):
        call_command("send_user_notifications", 5)
        self.notif.refresh_from_db()
        assert self.notif.consumed
