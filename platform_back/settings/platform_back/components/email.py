import logging

from platform_back.settings.environ import env

logger = logging.getLogger("django")

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@bimdata.io")

SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

if EMAIL_HOST := env("SMTP_HOST", default=None):
    EMAIL_PORT = env("SMTP_PORT", default=None)
    EMAIL_HOST_USER = env("SMTP_USER", default=None)
    EMAIL_HOST_PASSWORD = env("SMTP_PASS", default=None)
    EMAIL_USE_TLS = env.bool("SMTP_USE_TLS", default=True)
else:
    logger.warning("SMTP_HOST is not defined, the debugging emails will not be sent")


if APP_EMAIL_HOST := env("APP_SMTP_HOST", default=None):
    APP_EMAIL_PORT = env("APP_SMTP_PORT", default=None)
    APP_EMAIL_HOST_USER = env("APP_SMTP_USER", default=None)
    APP_EMAIL_HOST_PASSWORD = env("APP_SMTP_PASS", default=None)
    APP_EMAIL_USE_TLS = env.bool("APP_SMTP_USE_TLS", default=True)
else:
    logger.warning("APP_SMTP_HOST is not defined, use SMTP_HOST")

DEBUG_MAIL_TO = env("DEBUG_MAIL_TO", default="infra@bimdata.io")

ADMINS = [("Admin Platform-back", DEBUG_MAIL_TO)]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
