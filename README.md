# Migration 
python manage.py migrate
python manage.py makemigrations
python manage.py makemigrations models 

##setup crontab
python manage.py crontab add
python manage.py crontab show
python manage.py crontab remove
python manage.py crontab run <ID of crontab>



##Python guild
current_url = request.resolver_match.view_name
current_url = request.resolver_match.url_name
print(request.build_absolute_uri(current_url))

from django.urls import resolve
current_url = resolve(request.path_info).url_name
print(request.path_info)


# Celery
celery -A web _worker -l INFO
# Celery beat
celery -A web beat -l info -S django
or
celery -A web beat -l INFO --scheduler web_beat.schedulers:DatabaseScheduler

# Develop debug
celery -A web _worker --beat --scheduler django --loglevel=info


# check the system 
python manage.py check --database default
python manage.py check --database batch_log

#https://pypi.org/project/mysqlclient/