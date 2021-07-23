from os import environ
from os.path import dirname
from os.path import join

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv(join(dirname(__file__), "../../.env"))

ENV = environ.get("ENV", "development")
ADMIN_INTERFACE = environ.get("ADMIN_INTERFACE", "True")

_base_settings = [
    "../settings_base/components/*.py",
]

if "development" in ENV:
    _base_settings += ["../settings_base/environments/development.py"]
else:
    _base_settings += ["../settings_base/environments/production.py"]

if ADMIN_INTERFACE == "True":
    _base_settings += ["../settings_admin/common.py"]


# Include settings:
include(*_base_settings)
