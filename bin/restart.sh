ps -eux | grep gunicorn | awk '{print $2}' | xargs kill -9
python3 manage.py collectstatic
nohup gunicorn django_exercise.wsgi:application -c gunicorn_config.py &