# -*- coding: utf-8 -*-
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'update_weibo_follower_count': {
        'task': 'snh48.tasks.update_weibo_followers_count',
        'schedule': crontab(minute='28', hour='9'),
        'args': (),
        # 'options': {'queue': 'your_queue_name'},
    },
}