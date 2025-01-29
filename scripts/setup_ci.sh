#!/bin/bash
#
# Perform custom instructions then run tox `install_command` default value.
#
# Note:
# This script runs a custom operation to remove a pinned Django version spec in
# the requirements file used by tox for the base test environment. This prevents
# dependency resolution conflicts and allows `tox` to manage `Django` versions.
#
# Warning:
# This script is meant to be executed only by tox as an entry-point to the
# `install_command`. Executing this script manually or outside of this context
# may result in errors or other unknown side effects.

set -euo pipefail

# get the script's directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")
PROJECT_ROOT_DIR=$(dirname "$SCRIPT_DIR")

# Define the requirements directory and file
readonly REQUIREMENTS_DIR="$PROJECT_ROOT_DIR/requirements"
readonly CI_REQUIREMENTS_FILE="test-ci.txt"
readonly CI_REQUIREMENTS_PATH="$REQUIREMENTS_DIR/$CI_REQUIREMENTS_FILE"

# Ensure the requirements file exists.
if [[ ! -f "$CI_REQUIREMENTS_PATH" ]]; then
  echo "Error: Requirements file '$CI_REQUIREMENTS_FILE' not found." >&2
  exit 1
fi

# Verify the django package definition.
DJANGO_VERSION=$(
  grep -Ei '^django==[0-9]+\.[0-9]+\.[0-9]+' \
    "$CI_REQUIREMENTS_PATH" | head -n 1 || true
)

# Execute and output operation status message.
if [[ -n "$DJANGO_VERSION" ]]; then
  sed -i '/^django==[0-9]\+\.[0-9]\+\.[0-9]\+/I d' "$CI_REQUIREMENTS_PATH"
  echo "Removed $DJANGO_VERSION from requirements file, $CI_REQUIREMENTS_FILE"
fi

# ==============================================================================
# [Important] Run tox `install_command` with tox-provided substitution keys.
# ==============================================================================

python -I -m pip install "$@"
