"""Security settings for the project.

Centralize and manage all your security-related settings in this module.
This provides granular control to configure in target or all environments.

Thanks to blog by Adam Johnson!
See: https://adamj.eu/tech/2019/04/10/how-to-score-a+-for-security-headers-on-your-django-website/

For more details about this module
See: https://docs.djangoproject.com/en/4.2/topics/security/
"""

# ================ #
# X-XSS-Protection #
# ================ #
# Tell browser to block pages with detected XSS attacks.
SECURE_BROWSER_XSS_FILTER = True

# ========================= #
# Strict-Transport-Security #
# ========================= #
# Tell browser to load your site over HTTPS only.
# Note: Browsers will refuse to allow users to bypass insecure warnings to connect.
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ====================== #
# X-Content-Type-Options #
# ====================== #
# Tell browser to opt out of MIME Sniffing (guessing response content-type).
SECURE_CONTENT_TYPE_NOSNIFF = True

# =============== #
# Referrer-Policy #
# =============== #
# Tell browser to send `Referer` only for requests to the same domain.
SECURE_REFERRER_POLICY = "same-origin"

# =============== #
# X-Frame-Options #
# =============== #
# Tell browser to prevent site from being embedded into an <iframe>.
X_FRAME_OPTIONS = "DENY"

# ======= #
# SSL/TLS #
# ======= #
# Reverse proxy sets header `X-Forwarded-Host` to upstream service.
USE_X_FORWARDED_HOST = True

# Tell Django to trust `X-Forwarded-Host` from TLS terminating reverse proxy.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ======== #
# Sessions #
# ======== #
# Tell browser to ensure cookies are "secure" via transmission over HTTPS only.
SESSION_COOKIE_SECURE = True

# ==== #
# CSRF #
# ==== #
# Tell browser to ensure CSRF-cookies are "secure" via transmission over HTTPS only.
CSRF_COOKIE_SECURE = True
