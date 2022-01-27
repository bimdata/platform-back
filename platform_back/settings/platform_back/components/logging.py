import logging
import sys

from platform_back.settings.environ import env

CONSOLE_LOG_LEVEL = logging.INFO

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "[django] %(levelname)s %(asctime)s %(module)s %(message)s"
        }
    },
    "handlers": {
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "level": CONSOLE_LOG_LEVEL,
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
        # Warning messages are sent to admin emails
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "loggers": {
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.security.DisallowedHost": {"handlers": ["null"], "propagate": False},
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.template": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

FLUENTD_ENABLED = env.bool("FLUENTD_ENABLED", default=False)

if FLUENTD_ENABLED:
    FLUENTD_SERVER = env("FLUENTD_SERVER")
    FLUENTD_PORT = env.int("FLUENTD_PORT")
    FLUENTD_TAG = env("FLUENTD_TAG")
