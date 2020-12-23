import logging
from django.conf import settings
from fluent import handler

logger = logging.getLogger("platformback")
logger.setLevel(level=logging.INFO)
logHandler = handler.FluentHandler(
    settings.FLUENTD_TAG,
    host=settings.FLUENTD_SERVER,
    port=int(settings.FLUENTD_PORT),
    nanosecond_precision=True,
)
formatter = handler.FluentRecordFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


def log_user_connect(func):
    def wrapper(*args, **kwargs):
        user = func(*args, **kwargs)
        logger.info({"email": user.email, "action": "connect_to_platform", "message": f"{user.email} has just logged on to the platform"})

    return wrapper