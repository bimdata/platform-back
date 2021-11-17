from pathlib import Path

import environ

BASE_DIR = Path(__file__).parent.parent.parent
env = environ.Env()
env.read_env(BASE_DIR.joinpath(".env"))
