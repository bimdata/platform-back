# flake8: noqa E402
import sys

from platform_back.settings.environ import env

sys.path.append("platform_back/settings/platform_back/")

from components.common import INSTALLED_APPS
from components.common import MIDDLEWARE
from components.common import TEMPLATES

ENV = env("ENV")

if "development" in ENV:
    ENV_COLOR = "grey"
elif "staging" in ENV:
    ENV_COLOR = "green"
elif "next" in ENV:
    ENV_COLOR = "orange"
else:
    ENV_COLOR = "red"

GRAPPELLI_ADMIN_TITLE = "Platform Back Admin"
# Application definition
INSTALLED_APPS += [
    "grappelli",
    "grappelli.dashboard",
    "django.contrib.admin",
    "django.contrib.messages",
    "django.contrib.admindocs",
]

MIDDLEWARE += [
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

TEMPLATES[0]["OPTIONS"]["context_processors"] += [
    "django.contrib.messages.context_processors.messages",
    "platform_back.context_processors.from_settings",
]
