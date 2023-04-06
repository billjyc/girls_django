ps -eux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -9
ps -eux | grep celery | grep -v grep | awk '{print $2}' | xargs kill -9
python3 manage.py collectstatic
nohup celery -A django_exercise worker --loglevel=info > logs/celery_worker.log 2>&1 &
nohup celery -A django_exercise beat --loglevel=info > logs/celery_beat.log 2>&1 &
BUILD_ID=DONTKILLME nohup gunicorn django_exercise.wsgi:application -c gunicorn_config.py &

