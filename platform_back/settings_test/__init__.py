from os.path import dirname
from os.path import join

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv(join(dirname(__file__), "../../.env"))

_base_settings = [
    "../settings_base/components/*.py",
    "database.py",
    "common.py",
    "../settings_base/environments/development.py",
]

# Include settings:
include(*_base_settings)
