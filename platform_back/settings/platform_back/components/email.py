from platform_back.settings.environ import env

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@bimdata.io")

SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

if EMAIL_HOST := env("SMTP_HOST", default=None):
    EMAIL_PORT = env("SMTP_PORT", default=None)
    EMAIL_HOST_USER = env("SMTP_USER", default=None)
    EMAIL_HOST_PASSWORD = env("SMTP_PASS", default=None)
    EMAIL_USE_TLS = env.bool("SMTP_USE_TLS", default=True)

DEBUG_MAIL_TO = env("DEBUG_MAIL_TO", default="infra@bimdata.io")

ADMINS = [("Admin Platform-back", DEBUG_MAIL_TO)]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
