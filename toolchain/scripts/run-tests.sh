#!/bin/bash

set -o errexit
set -o verbose

targets=(service main.py)

# Find common security issues (https://bandit.readthedocs.io)
bandit --recursive "${targets[@]}"

# Python code formatter (https://black.readthedocs.io)
black --check --diff "${targets[@]}"

# Style guide enforcement (https://flake8.pycqa.org)
flake8 --config toolchain/config/.flake8 "${targets[@]}"

# Sort imports (https://pycqa.github.io/isort)
isort --src . --settings-path toolchain/config/.isort.cfg --check --diff "${targets[@]}"

# Static type checker (https://mypy.readthedocs.io)
mypy --config-file toolchain/config/.mypy.ini "${targets[@]}"

# Check for errors, enforce a coding standard, look for code smells (http://pylint.pycqa.org)
pylint --rcfile toolchain/config/.pylintrc "${targets[@]}"

# Check dependencies for security issues (https://pyup.io/safety)
safety check -r requirements.txt -r requirements-dev.txt

# Report code complexity (https://radon.readthedocs.io)
radon mi "${targets[@]}"

# Exit with non-zero status if code complexity exceeds thresholds (https://xenon.readthedocs.io)
xenon --max-absolute A --max-modules A --max-average A "${targets[@]}"
