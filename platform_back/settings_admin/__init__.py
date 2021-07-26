from os import environ
from os.path import dirname
from os.path import join

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv(join(dirname(__file__), "../../.env"))

ENV = environ.get("ENV", "development")

_base_settings = [
    "../settings_base/components/*.py",
    "./*.py",
    "../settings_base/environments/production.py",
]

# Include settings:
include(*_base_settings)
