import logging

PASSWORD_HASHERS = (
    "django.contrib.auth.hashers.MD5PasswordHasher",  # Replace hasher with a simpler and faster hash method
)
DEBUG = False
TESTING = True
ADMIN_INTERFACE = False


# Disable migration during testsuite
class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()  # Disable migrations during tests
MEDIA_ROOT = "/tmp/django-tests"
MEDIA_URL = "/media/"

logging.disable(logging.INFO)

# Use default logger during tests
LOGGING = None


DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
