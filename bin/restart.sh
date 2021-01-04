ps -eux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -9
ROOT_DIR=".."
python3 ${ROOT_DIR}/manage.py collectstatic
BUILD_ID=DONTKILLME nohup gunicorn django_exercise.wsgi:application -c ${ROOT_DIR}/gunicorn_config.py &