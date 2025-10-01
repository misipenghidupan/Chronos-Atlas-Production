#!/bin/bash
# Setup Python environment for Chronos Atlas using pyenv and virtualenv
# Usage: ./scripts/setup_python_env.sh

set -e

PYTHON_VERSION=3.11.0
VENV_NAME=chronosatlas-dev

# Install Python version if not present
if ! pyenv versions --bare | grep -q "$PYTHON_VERSION"; then
  pyenv install "$PYTHON_VERSION"
fi

# Create virtualenv if not present
if ! pyenv virtualenvs --bare | grep -q "$VENV_NAME"; then
  pyenv virtualenv "$PYTHON_VERSION" "$VENV_NAME"
fi

# Set local virtualenv
pyenv local "$VENV_NAME"

# Install requirements
pip install -r requirements.txt

echo "Python environment '$VENV_NAME' with $PYTHON_VERSION is ready."
