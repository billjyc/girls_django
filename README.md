## 启动
* `nohup gunicorn django_exercise.wsgi:application -c gunicorn_config.py &
`

## 静态文件修改
* 静态资源目录在`settings.py`中的`STATIC_ROOT`变量配置
* 如果静态资源文件发生变化，需要执行`python3 manage.py collectstatic`来刷新