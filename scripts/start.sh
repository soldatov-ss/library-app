#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

python3 wait_for_postgres.py

python3 manage.py migrate
python manage.py runserver 0.0.0.0:8000