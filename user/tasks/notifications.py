from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)


@shared_task
def send_user_notifications(notification_delay_minutes):
    call_command("send_user_notifications", notification_delay_minutes)
    logger.info(("All user notifications have been send"))
