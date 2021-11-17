from django.core.exceptions import ImproperlyConfigured
from split_settings.tools import include

from platform_back.settings.environ import env

ADMIN_INTERFACE = env.bool("ADMIN_INTERFACE", default=False)
if ADMIN_INTERFACE:
    raise ImproperlyConfigured(
        "Environment variable 'ADMIN_INTERFACE' must not be set, or set to false"
    )


ENV = env("ENV")

_base_settings = [
    "../platform_back/components/*.py",
    "./*.py",
    "../platform_back/environments/production.py",
]

# Include settings:
include(*_base_settings)
