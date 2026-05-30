import os

from .base import *  # noqa: F403,F401
from .base import env_bool, env_list

DEBUG = False

# Serve hashed, compressed static files via WhiteNoise in production.
STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Required in production — fail loudly if missing.
SECRET_KEY = os.environ["SECRET_KEY"]

# --- Allowed hosts -----------------------------------------------------------
# Resilient by default: whatever you set in ALLOWED_HOSTS, PLUS Railway's
# auto-provided public domain, its health-check host, and any *.up.railway.app
# subdomain. This means the app boots and passes Railway's health check even if
# the ALLOWED_HOSTS env var is empty or not yet configured.
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "")
_railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip()
if _railway_domain:
    ALLOWED_HOSTS.append(_railway_domain)
ALLOWED_HOSTS += ["healthcheck.railway.app", ".up.railway.app"]
ALLOWED_HOSTS = list(dict.fromkeys(h for h in ALLOWED_HOSTS if h))  # de-dupe, drop blanks

# --- CSRF --------------------------------------------------------------------
# Railway terminates TLS at the proxy; trust the forwarded scheme header.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "")
if _railway_domain:
    CSRF_TRUSTED_ORIGINS.append(f"https://{_railway_domain}")
CSRF_TRUSTED_ORIGINS.append("https://*.up.railway.app")
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(o for o in CSRF_TRUSTED_ORIGINS if o))

# --- HTTPS / hardening -------------------------------------------------------
# HTTP->HTTPS redirect is OFF by default so Railway's (HTTP) health check gets a
# 200 instead of a 301. Railway already serves the public domain over HTTPS, and
# HSTS below still forces HTTPS in browsers. Turn the redirect on once you're on
# a stable custom domain by setting SECURE_SSL_REDIRECT=true in Railway.
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", False)
# Never redirect the health-check endpoint, even when the redirect is enabled.
SECURE_REDIRECT_EXEMPT = [r"^healthz/?$"]

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
