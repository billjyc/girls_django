#!/bin/bash
ps -eux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -9
ps -eux | grep celery | grep -v grep | awk '{print $2}' | xargs kill -9
pwd
cd /home/ubuntu/Documents/girls_django
./venv/bin/python3 manage.py collectstatic --noinput
mkdir -p logs
nohup ./venv/bin/celery -A django_exercise worker --loglevel=info > logs/celery_worker.log 2>&1 &
nohup ./venv/bin/celery -A django_exercise beat --loglevel=info > logs/celery_beat.log 2>&1 &
BUILD_ID=DONTKILLME ./venv/bin/gunicorn django_exercise.wsgi:application -c gunicorn_config.py

