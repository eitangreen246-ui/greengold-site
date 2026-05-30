import os

from .base import *  # noqa: F403,F401

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# A throwaway key is fine for local development only.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-only-key-change-me-0e+$sz@%()r%2q5fr5#keb9vn",
)

ALLOWED_HOSTS = ["*"]

try:
    from .local import *  # noqa: F403,F401
except ImportError:
    pass
