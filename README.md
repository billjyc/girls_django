## Docker打包方法
* 登录docker hub：`docker login`
* 打包：`docker build -t billjyc/girls_django:latest . --platform linux/amd64`
* 上传：`docker push billjyc/girls_django:latest`

## 启动
* `nohup gunicorn django_exercise.wsgi:application -c gunicorn_config.py &`
* docker启动方法：`docker run -d -p 8099:8099 -v /data/logs/girls_django/:/usr/app/logs billjyc/girls_django:latest`
`

## 本地数据库迁移
* `python manage.py migrate`
* 如果数据库切换，在DBeaver上操作会提示无权限，需要进命令行操作
  * `mysql> create database abc;      # 创建数据库 `
  * `mysql> use abc;                  # 使用已创建的数据库 `
  * `mysql> set names utf8;           # 设置编码` 
  * `mysql> source /home/abc/abc.sql  # 导入备份数据库`


## 静态文件修改
* 静态资源目录在`settings.py`中的`STATIC_ROOT`变量配置
* 如果静态资源文件发生变化，需要执行`python3 manage.py collectstatic`来刷新