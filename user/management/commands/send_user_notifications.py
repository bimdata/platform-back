import logging
from datetime import timedelta

from django.core.management.base import BaseCommand

from django.db.models import Max
from django.db.models import Q
from django.utils import timezone

from user.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Send user notifations"

    def add_arguments(self, parser):
        parser.add_argument(
            "notification_delay_minutes",
            type=int,
            help="Number of minute to wait before sending the notification, for grouping",
        )

    def handle(self, *args, **options):
        users = User.objects.annotate(
            last_notif=Max("notification__created_at", filter=Q(notification__consumed=False))
        ).filter(
            last_notif__lt=timezone.now()
            - timedelta(minutes=options["notification_delay_minutes"])
        )

        for user in users:
            logger.info("Sending email notification to user %s", user)
            user.send_email_notifications()
            if len(users):
                return "Send notifications to " + ", ".join([user.email for user in users])
            else:
                return "No notifications to send"
