import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "platform_back.settings.platform_back")

app = Celery("platform_back")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()
