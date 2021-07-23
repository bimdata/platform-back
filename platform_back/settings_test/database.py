from os import environ


DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": environ.get("TEST_DB_NAME", "platform_backtest"),
        "USER": environ.get("TEST_DB_USER", "platform_back"),
        "PASSWORD": environ.get("TEST_DB_PASSWORD", "platform_back"),
        "HOST": environ.get("TEST_DB_HOST", "127.0.0.1"),
        "PORT": environ.get("TEST_DB_PORT", "5432"),
    }
}
