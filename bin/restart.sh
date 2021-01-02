ps -eux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -9
python3 manage.py collectstatic
BUILD_ID=DONTKILLME nohup gunicorn django_exercise.wsgi:application -c gunicorn_config.py &