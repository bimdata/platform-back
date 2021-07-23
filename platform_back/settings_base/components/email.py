from os import environ

DEFAULT_FROM_EMAIL = environ.get("DEFAULT_FROM_EMAIL", "support@bimdata.io")

SERVER_EMAIL = "bug@bimdata.io"
EMAIL_HOST = environ.get("SMTP_HOST", "smtp.mandrillapp.com")
EMAIL_HOST_PASSWORD = environ.get("SMTP_PASS", environ.get("MANDRILL_SMTP_KEY", False))
EMAIL_HOST_USER = environ.get("SMTP_USER", "BIMData.io")
EMAIL_PORT = environ.get("SMTP_PORT", 587)
EMAIL_USE_TLS = environ.get("SMTP_USE_TLS", "True") == "True"

ADMINS = [("infra", "infra@bimdata.io")]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
