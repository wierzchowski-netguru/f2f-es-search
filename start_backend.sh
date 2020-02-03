#!/usr/bin/env ash


set -o errexit
set -o pipefail
set -o nounset

python manage.py wait_for_postgres 10
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
