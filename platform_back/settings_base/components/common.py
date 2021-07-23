from os import environ

from corsheaders.defaults import default_headers
from platform_back.settings_base.components import BASE_DIR


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

ENV = environ.get("ENV", "development")
ADMIN_INTERFACE = environ.get("ADMIN_INTERFACE", "True")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get("SECRET_KEY", "7rvr*q1&_eqcetu^2x#2q+4&g8(&n&6*68+6xd#mxqs^6-u2rp")

API_URL = environ.get("API_URL", "http://localhost:8081")
APP_URL = environ.get("APP_URL", "http://localhost:8080")
PLATFORM_BACK_URL = environ.get("PLATFORM_BACK_URL", "http://127.0.0.1:8082")

WEBHOOKS_SECRET = environ.get("WEBHOOKS_SECRET", "123")

REQUESTS_CA_BUNDLE = environ.get("REQUESTS_CA_BUNDLE", "")

if environ.get("ALLOWED_HOSTS"):
    ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS").split(",")


INSTALLED_APPS = [
    "user",
    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "health_check",
    "health_check.db",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "psqlextra",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = default_headers + ("Content-Encoding",)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


ROOT_URLCONF = "platform_back.urls"
WSGI_APPLICATION = "platform_back.wsgi.application"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = "statics"


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

DEFAULT_AUTHENTICATION_CLASSES = (
    "oidc_auth.authentication.JSONWebTokenAuthentication",
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
    "DEFAULT_FILTER_BACKENDS": ("utils.contrib.drf.filters.FilterBackendWithQuerysetWorkaround",),
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

TIME_ZONE = "UTC"

BCF_DATE_FORMAT = ("%m/%d/%Y",)

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = False

SWAGGER_SETTINGS = {
    "DEEP_LINKING": True,
    "DEFAULT_AUTO_SCHEMA_CLASS": "utils.doc.CamelCaseOperationIDAutoSchema",
    "DEFAULT_FILTER_INSPECTORS": ["utils.filters.DjangoFilterDescriptionInspector"],
    "DOC_EXPANSION": "none",
    "OPERATIONS_SORTER": "alpha",
    "TAGS_SORTER": "alpha",
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "description": 'Copy/paste a valid access token here prefixed with "Bearer "',
            "name": "Authorization",
            "in": "header",
        }
    },
    "USE_SESSION_AUTH": False,
    "DEFAULT_INFO": "utils.doc.API_INFO",
    "DEFAULT_API_URL": "https://api.bimdata.io/doc",
}

MASTER_TOKEN = environ.get("MASTER_TOKEN", "123")
