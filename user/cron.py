import logging
from datetime import timedelta

from django.conf import settings
from django.db.models import Max
from django.db.models import Q
from django.utils import timezone
from django_cron import CronJobBase
from django_cron import Schedule

from user.models import User

logger = logging.getLogger(__name__)


class SendEmailNotifJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 1 min

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "user.send_email_notif_job"  # a unique code

    def do(self):
        users = User.objects.annotate(
            last_notif=Max("notification__created_at", filter=Q(notification__consumed=False))
        ).filter(last_notif__lt=timezone.now() - timedelta(minutes=settings.NOTIFS_DELAY))

        for user in users:
            logger.info("Sending email notification to user %s", user)
            user.send_email_notifications()
        if len(users):
            return "Send notifications to " + ", ".join([user.email for user in users])
        else:
            return "No notifications to send"
