# -*- coding: utf-8 -*-
import json
import logging

from celery import shared_task

from django_exercise.weibo_util import weibo_client
from .models import Weibo, WeiboDataHistory, Memberinfo

logger = logging.getLogger(__name__)


@shared_task
def update_weibo_followers_count():
    # 获取需要更新的用户列表
    users = Weibo.objects.filter()
    logger.info("start update weibo fans count, total: {}".format(len(users)))
    for user in users:
        data = weibo_client.get_user_info(user.weibo_id)
        logger.info("update weibo fans count, weibo_id: {}, data: {}".format(user.weibo_id, json.dumps(data)))
        # 更新数据库中的粉丝数
        user.followers_count = data['followers_count']
        user.friends_count = data['friends_count']
        user.statuses_count = data['statuses_count']
        user.save()

        # 保存历史数据
        weibo_data_history = WeiboDataHistory()
        weibo_data_history.member_id = user.id
        weibo_data_history.weibo_id = user.weibo_id
        weibo_data_history.followers_count = data['followers_count']
        weibo_data_history.friends_count = data['friends_count']
        weibo_data_history.statuses_count = data['statuses_count']
        weibo_data_history.save()

