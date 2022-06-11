python3 manage.py collectstatic
mkdir logs
gunicorn django_exercise.wsgi:application -c gunicorn_config.py

tail -f /dev/null