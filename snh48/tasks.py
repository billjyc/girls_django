# -*- coding: utf-8 -*-
import json
import logging
import time
from datetime import datetime

from celery import shared_task

from utils.browser_manager import browser_manager
from utils.weibo_util import weibo_client
from snh48.models import Weibo, WeiboDataHistory

logger = logging.getLogger(__name__)


@shared_task
def update_weibo_followers_count():
    # 获取需要更新的用户列表
    users = Weibo.objects.filter()
    logger.info("start update weibo fans count, total: {}".format(len(users)))
    try:
        for user in users:
            try:
                time.sleep(0.5)
                # 获取当前日期时间
                now = datetime.now()
                # 将当前日期时间格式化为字符串
                current_datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
                data = weibo_client.get_user_info_2(user.weibo_id)
                logger.info("update weibo fans count, user id: {}, weibo_id: {}, data: {}".format(user.id, user.weibo_id, json.dumps(data)))
                # 更新数据库中的粉丝数
                user.followers_count = data['data']['user']['followers_count']
                user.friends_count = data['data']['user']['friends_count']
                user.statuses_count = data['data']['user']['statuses_count']
                user.update_time = current_datetime_str
                user.save()

                # 保存历史数据
                weibo_data_history = WeiboDataHistory()
                weibo_data_history.member_id = user.id
                weibo_data_history.weibo_id = user.weibo_id
                weibo_data_history.followers_count = data['data']['user']['followers_count']
                weibo_data_history.friends_count = data['data']['user']['friends_count']
                weibo_data_history.statuses_count = data['data']['user']['statuses_count']
                weibo_data_history.update_time = current_datetime_str
                weibo_data_history.save()
            except Exception as e:
                continue
    finally:
        browser_manager.close()

if __name__ == '__main__':
    update_weibo_followers_count()
