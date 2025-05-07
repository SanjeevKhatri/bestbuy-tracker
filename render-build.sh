#!/usr/bin/env bash

# Use virtual environment Python if available
VENV_PY=$(which python)

# Install Playwright and browser dependencies
$VENV_PY -m playwright install --with-deps
