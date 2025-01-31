#!/bin/sh

set -e

# Apply database migrations.
python manage.py migrate --no-input

exec "$@"
