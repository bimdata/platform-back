from split_settings.tools import include

from platform_back.settings.environ import env

ENV = env("ENV")
ADMIN_INTERFACE = env.bool("ADMIN_INTERFACE")

_base_settings = [
    "components/*.py",
]

if "development" in ENV:
    _base_settings += ["environments/development.py"]
else:
    _base_settings += ["environments/production.py"]

if ADMIN_INTERFACE:
    _base_settings += ["../admin/common.py"]


# Include settings:
include(*_base_settings)
