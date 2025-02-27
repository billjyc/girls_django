python3 manage.py collectstatic --noinput
mkdir -p logs
nohup celery -A django_exercise worker --loglevel=info > logs/celery_worker.log 2>&1 &
nohup celery -A django_exercise beat --loglevel=info > logs/celery_beat.log 2>&1 &
gunicorn django_exercise.wsgi:application -c gunicorn_config.py

tail -f /dev/null