# flake8: noqa E402
import logging
import os
import sys

sys.path.append("platform_back/settings/platform_back/")


from components.common import INSTALLED_APPS
from components.common import MIDDLEWARE
from components.logging import LOGGING

CONSOLE_LOG_LEVEL = logging.DEBUG
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = ["*"]

LOGGING["handlers"]["console"]["level"] = CONSOLE_LOG_LEVEL
