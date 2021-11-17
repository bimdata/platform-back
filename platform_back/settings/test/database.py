from platform_back.settings.environ import env

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": env("TEST_DB_NAME"),
        "USER": env("TEST_DB_USER"),
        "PASSWORD": env("TEST_DB_PASSWORD"),
        "HOST": env("TEST_DB_HOST"),
        "PORT": env("TEST_DB_PORT"),
    }
}
