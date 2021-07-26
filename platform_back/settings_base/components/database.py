from os import environ

from platform_back.settings_base.components.common import ADMIN_INTERFACE
from platform_back.settings_base.components.common import MIDDLEWARE


DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": environ.get("DB_NAME", "platform_back"),
        "USER": environ.get("DB_USER", "platform_back"),
        "PASSWORD": environ.get("DB_PASSWORD", "platform_back"),
        "HOST": environ.get("DB_HOST", "127.0.0.1"),
        "PORT": environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 600,
    }
}

if environ.get("REPLICA_DB_HOSTS"):
    from django_replicated.settings import *  # noqa F401,F403

    MIDDLEWARE += ["django_replicated.middleware.ReplicationMiddleware"]
    DATABASE_ROUTERS = ["django_replicated.router.ReplicationRouter"]
    REPLICATED_DATABASE_SLAVES = []
    REPLICATED_DATABASE_DOWNTIME = 60
    if ADMIN_INTERFACE == "True":
        REPLICATED_VIEWS_OVERRIDES = {
            "/admin/*/change/": "master",
            "/admin/*/add/": "master",
            "/admin/*/delete/": "master",
        }

    r_db_hosts = environ.get("REPLICA_DB_HOSTS").split(",")
    r_db_ports = environ.get("REPLICA_DB_PORTS").split(",")

    r_db_names = (
        names.split(",")
        if (names := environ.get("REPLICA_DB_NAMES"))
        else [DATABASES["default"]["NAME"]] * len(r_db_hosts)
    )
    r_db_users = (
        users.split(",")
        if (users := environ.get("REPLICA_DB_USERS"))
        else [DATABASES["default"]["USER"]] * len(r_db_hosts)
    )
    r_db_passwords = (
        passwords.split(",")
        if (passwords := environ.get("REPLICA_DB_PASSWORDS"))
        else [DATABASES["default"]["PASSWORD"]] * len(r_db_hosts)
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
