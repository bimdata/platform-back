import logging
import os

from platform_back.settings_base.components.common import INSTALLED_APPS
from platform_back.settings_base.components.common import MIDDLEWARE
from platform_back.settings_base.components.logging import LOGGING

CONSOLE_LOG_LEVEL = logging.DEBUG
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True
MEDIA_ROOT = os.path.join(os.getenv("HOME"), "django-media-dev")
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)
MEDIA_URL = "/media/"

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "[::1]",
]

LOGGING["handlers"]["console"]["level"] = CONSOLE_LOG_LEVEL
