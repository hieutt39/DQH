#!/bin/sh

# python manage.py flush --no-input
python manage.py migrate
#python manage.py collectstatic --no-input --clear

# register crontab
#python manage.py crontab remove
#python manage.py crontab add

exec "$@"