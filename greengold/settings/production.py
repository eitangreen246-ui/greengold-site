import os

from .base import *  # noqa: F403,F401
from .base import env_bool, env_list

DEBUG = False

# Serve hashed, compressed static files via WhiteNoise in production.
STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Required in production — fail loudly if missing.
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "")

# Railway terminates TLS at the proxy; trust the forwarded header.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "")

# Hardening (toggle-able via env so health checks / first boot don't lock out).
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "2592000"))  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

try:
    from .local import *  # noqa: F403,F401
except ImportError:
    pass
