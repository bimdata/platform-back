from corsheaders.defaults import default_headers

from platform_back.settings.environ import BASE_DIR
from platform_back.settings.environ import env


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

DEBUG = env.bool("DEBUG", False)
SECRET_KEY = env("SECRET_KEY", default="SET_DEVELOPMENT_DJANGO_SECRET_KEY")

API_URL = env("API_URL", default="")
PLATFORM_URL = env("PLATFORM_URL", default="")
PLATFORM_BACK_URL = env("PLATFORM_BACK_URL", default="")

WEBHOOKS_SECRET = env("WEBHOOKS_SECRET", default="")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


INSTALLED_APPS = [
    "user",
    "webhooks",
    "notification",
    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "health_check",
    "health_check.db",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "psqlextra",
    "django_cron",
    "celery",
    "django_celery_beat",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CRON_CLASSES = ["user.cron.SendEmailNotifJob"]

NOTIFS_DELAY = env.int("NOTIFS_DELAY", default=5)  # minutes

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = default_headers + ("Content-Encoding",)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SSL_CERT_FILE = env("SSL_CERT_FILE", default=None)

ROOT_URLCONF = "platform_back.urls"
WSGI_APPLICATION = "platform_back.wsgi.application"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = "statics"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.joinpath("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ]
        },
    }
]

DEFAULT_AUTHENTICATION_CLASSES = ("oidc_auth.authentication.JSONWebTokenAuthentication",)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
    "DEFAULT_FILTER_BACKENDS": (
        "utils.contrib.drf.filters.FilterBackendWithQuerysetWorkaround",
    ),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%SZ",
    "URL_FORMAT_OVERRIDE": None,
}


PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher"]


AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

AUTH_USER_MODEL = "user.User"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"
LOCALE_PATHS = [BASE_DIR.joinpath("locale")]

TIME_ZONE = "UTC"

BCF_DATE_FORMAT = ("%m/%d/%Y",)

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = False
