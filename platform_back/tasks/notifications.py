from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command


logger = get_task_logger(__name__)


@shared_task
def send_project_notifications_email(project_id):
    call_command("send_notification_email", project_id)
    logger.info("Old flagged entities have been deleted")
