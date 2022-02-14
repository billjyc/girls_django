python3 manage.py collectstatic
gunicorn django_exercise.wsgi:application -c gunicorn_config.py

tail -f /dev/null