#!/usr/bin/env sh

set -o errexit
set -o nounset

cd /code && pipenv sync
find /code -name "*.pyc" -delete
cd src
pytest -v .
