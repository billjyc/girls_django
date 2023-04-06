# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_exercise.settings')

# 创建Celery实例并指定名称
app = Celery('SNH48')

# 使用Django的设置文件配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
