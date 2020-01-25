# -*- coding:utf-8 -*-
"""
微信小经费
"""

import json
import logging
import time

import requests
from urllib.parse import unquote

my_logger = logging.getLogger(__name__)
#
# from modian.modian_card_draw import handler as card_draw_handler

# from modian.special import modian_wufu_handler
# from qq.qqhandler import QQHandler
# from utils import global_config, util
# from utils.mysql_util import mysql_util


class GroupAccountEntity:
    def __init__(self, link, title, group_account_id, broadcast_groups=[], qrcode='', current=0.0, support_num=0):
        self.link = link
        self.title = title
        self.group_account_id = group_account_id
        # self.need_display_rank = need_display_rank
        self.broadcast_groups = broadcast_groups
        self.qrcode = qrcode
        self.current = current
        # self.target = target
        self.support_num = support_num


class WeixinGroupAccountHandler:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, group_account_notify_groups, group_account_project_array):
        self.session = requests.session()
        self.group_account_notify_groups = group_account_notify_groups
        self.group_account_project_array = group_account_project_array

        # self.card_draw_handler = card_draw_handler
        self.order_queues = {}

    def init_order_queues(self):
        for group_account_entity in self.group_account_project_array:
            try:
                my_logger.info('初始化%s的订单队列', group_account_entity.group_account_id)
                my_logger.debug(self.order_queues)
                if group_account_entity.group_account_id not in self.order_queues:
                    self.order_queues[group_account_entity.group_account_id] = set()
                    my_logger.debug('队列为空，重新初始化队列')
                else:
                    my_logger.debug('队列不为空，不重新初始化队列')
                    continue
                my_logger.debug('项目%s队列长度: %s', group_account_entity.group_account_id,
                                len(self.order_queues[group_account_entity.group_account_id]))

                orders = self.query_project_orders(group_account_entity)

                for order in orders:
                    listid = int(order['listid'])
                    self.order_queues[group_account_entity.group_account_id].add(listid)
            except Exception as e:
                my_logger.error('初始化订单队列失败！')
                my_logger.exception(e)

    def weixin_header(self):
        """
        header信息
        """
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'grp_qlskey=v0ae789cc115e00b0a1c1ca186f09b45;grp_qluin=91be027df85334c678b99fe50566e8eb',  # cookie要换成自己的
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI Language/zh_CN',
        }
        return header

    def get_all_orders(self, group_account_entity):
        """
        获取所有订单
        :return:
        """
        orders = []
        page = 1
        lastbkid = ''
        while True:
            sub_order = self.query_project_orders(group_account_entity, page, 20, lastbkid)
            if sub_order:
                orders.extend(sub_order)
            else:
                break
            page += 1
            lastbkid = sub_order[len(sub_order) - 1]['bkid']
        return orders

    def query_project_orders(self, group_account_entity, page=1, limit=10, lastbkid=''):
        """
        批量获取订单
        :param group_account_entity:
        :param page:
        :param limit:
        :return:
        """
        my_logger.info('查询项目订单, id: %s', group_account_entity.group_account_id)
        url = 'https://groupaccount.tenpay.com/fcgi-bin/grp_qry_group_water.fcgi'
        data = {
            "group_account_id": group_account_entity.group_account_id,
            "start_time": '2017-01-01 00:00:00',
            "end_time": '2100-01-31 00:00:00',
            "qry_ver": 1,
            "lastbkid": lastbkid,
            "offset": 0,
            "limit": limit,
            "type": 2,
            "target_unionid": ""
        }
        r = self.session.post(url=url, data=data, headers=self.weixin_header()).json()
        if int(r['retcode']) != 0:
            raise RuntimeError('获取订单信息失败')
        orders = json.loads(unquote(r['water_array']))
        my_logger.info('项目订单: page: %s, orders: %s', page, orders)
        return orders['water_array']

    def get_current_and_target(self, group_account_entity):
        """
        查询当前项目情况
        :param group_account_entity:
        :return:
        """
        my_logger.info('获取当前进度和总额: pro_id: %s', group_account_entity.group_account_id)
        api = 'https://groupaccount.tenpay.com/fcgi-bin/grp_qry_group_info.fcgi'
        data = {
            "group_account_id": group_account_entity.group_account_id
        }
        r = self.session.post(api, data=data, headers=self.weixin_header()).json()
        if int(r['retcode']) == 0:
            name = r['name']
            current = float(r['balance']) / 100
            user_num = r['user_num']
            my_logger.info('支持人数: %s, 当前进度: %s', user_num, current)
            return name, current, user_num
        else:
            raise RuntimeError('获取项目筹款结果查询失败')


if __name__ == "__main__":
    entity = GroupAccountEntity('ssss', '400场', '4mr9Xz920100009000043331')
    handler = WeixinGroupAccountHandler([], [entity])
    handler.init_order_queues()
    # orders = handler.query_project_orders(entity)
    pass

