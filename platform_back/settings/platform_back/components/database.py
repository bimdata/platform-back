# flake8: noqa E402
import sys

from platform_back.settings.environ import env

sys.path.append("platform_back/settings/platform_back/")

from components.common import MIDDLEWARE

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "CONN_MAX_AGE": 600,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

if env.list("REPLICA_DB_HOSTS", default=None):
    from django_replicated.settings import *  # noqa F401,F403

    MIDDLEWARE += ["django_replicated.middleware.ReplicationMiddleware"]
    DATABASE_ROUTERS = ["django_replicated.router.ReplicationRouter"]
    REPLICATED_DATABASE_SLAVES = []
    REPLICATED_DATABASE_DOWNTIME = 60
    if env.bool("ADMIN_INTERFACE", default=False):
        REPLICATED_VIEWS_OVERRIDES = {
            "/admin/*/change/": "master",
            "/admin/*/add/": "master",
            "/admin/*/delete/": "master",
        }

    r_db_hosts = env.list("REPLICA_DB_HOSTS")
    r_db_ports = env.list(
        "REPLICA_DB_PORTS", default=[DATABASES["default"]["PORT"]] * len(r_db_hosts)
    )
    r_db_names = env.list(
        "REPLICA_DB_NAMES", default=[DATABASES["default"]["NAME"]] * len(r_db_hosts)
    )
    r_db_users = env.list(
        "REPLICA_DB_USERS", default=[DATABASES["default"]["USER"]] * len(r_db_hosts)
    )
    r_db_passwords = env.list(
        "REPLICA_DB_PASSWORDS", default=[DATABASES["default"]["PASSWORD"]] * len(r_db_hosts)
    )

    for i, (host, port, name, user, password) in enumerate(
        zip(r_db_hosts, r_db_ports, r_db_names, r_db_users, r_db_passwords)
    ):
        DATABASES[f"replica_{i}"] = {
            "ENGINE": "psqlextra.backend",
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "HOST": host,
            "PORT": port,
            "CONN_MAX_AGE": 600,
        }
        REPLICATED_DATABASE_SLAVES += [f"replica_{i}"]
