from platform_back.settings.environ import env

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@bimdata.io")

SERVER_EMAIL = env("DEBUG_MAIL_TO", default="bug@bimdata.io")

if EMAIL_HOST := env("SMTP_HOST", default=None):
    EMAIL_PORT = env("SMTP_PORT")
    EMAIL_HOST_USER = env("SMTP_USER")
    EMAIL_HOST_PASSWORD = env("SMTP_PASS")
    EMAIL_USE_TLS = env.bool("SMTP_USE_TLS")

ADMINS = [("infra", "infra@bimdata.io")]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
