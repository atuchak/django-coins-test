#!/usr/bin/env sh

set -o errexit
set -o nounset


export DJANGO_ENV

cd /code && pipenv sync
python /code/src/manage.py migrate --noinput

python -Wd /code/src/manage.py runserver 0.0.0.0:8000
