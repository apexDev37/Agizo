"""Environment `service` settings for the config project.

The environment variables defined here are for service or third-parties
to create isolation in relation to other Django project settings.

Example:
    - This may include defining keys or configs for other external services
    such as: `AWS_ACCESS_KEY`, `GOOGLE_CLOUD_PROJECT`, `GITHUB_TOKEN`, etc.
"""

from pathlib import Path

import environ

from config.settings.common.base import BASE_DIR

# Set module-level ENV default casting.
env = environ.FileAwareEnv(
    AFRICAS_TALKING_USERNAME=(str, "sandbox"),
    AFRICAS_TALKING_API_KEY=(str, None),
    OIDC_RP_CLIENT_ID=(str, None),
    OIDC_RP_CLIENT_SECRET=(str, None),
)

# Read environment variables from .env file.
# We explicitly do not want to override the above
# envs where we also supply envs at the infra-level (Compose)
# or another level directly on the host environment.
environ.Env.read_env(
    Path(BASE_DIR, ".envs", "service.env"),
    overwrite=False,
)

# africastalking
AFRICAS_TALKING_USERNAME = env("AFRICAS_TALKING_USERNAME")
AFRICAS_TALKING_API_KEY = env("AFRICAS_TALKING_API_KEY")

# mozilla_django_oidc
OIDC_RP_CLIENT_ID = env("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = env("OIDC_RP_CLIENT_SECRET")
