#!/bin/sh

# wait for postgres
sleep 10

python manage.py migrate --no-input

python manage.py collectstatic --no-input

exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 config.wsgi:application