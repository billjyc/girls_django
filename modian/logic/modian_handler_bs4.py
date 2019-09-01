# -*- coding:utf-8 -*-
"""
六选之后，摩点关闭了粉丝应援类项目，API就不能使用了，在这里临时改为直接爬取网页
"""

import json
import logging
import time

import requests
from bs4 import BeautifulSoup


my_logger = logging.getLogger(__name__)



class ModianEntity:
    def __init__(self, link, title, pro_id, need_display_rank=False, broadcast_groups=[], current=0.0, target=0.0,
                 support_num=0):
        self.link = link
        self.title = title
        self.pro_id = pro_id
        self.need_display_rank = need_display_rank
        self.broadcast_groups = broadcast_groups
        self.current = current
        self.target = target
        self.support_num = support_num
        # 以下的2个参数很重要，获取订单时需要使用
        self.pro_class = 201
        self.post_id = 0


class ModianHandlerBS4:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, modian_notify_groups, modian_project_array):
        self.session = requests.session()
        self.modian_notify_groups = modian_notify_groups
        self.modian_project_array = modian_project_array

    def get_project_profiles(self, modian_entity):
        """
        获取集资项目基本资料
        :param modian_entity:
        :return:
        """
        my_logger.info('获取集资项目基本资料, 摩点id: {}'.format(modian_entity.pro_id))
        url = 'https://zhongchou.modian.com/realtime/get_simple_product?jsonpcallback=jQuery1_1&ids={}&if_all=1&_=2'.format(
            modian_entity.pro_id)
        rsp = self.session.get(url, headers=self.modian_header()).text
        # 中间结果是个json字符串，需要把头尾过滤掉
        rsp = rsp[41: -3]
        my_logger.info('返回结果: {}'.format(rsp))
        project_profile_json = json.loads(rsp, encoding='utf-8')
        modian_entity.pro_class = project_profile_json['pro_class']
        modian_entity.target = project_profile_json['goal']
        modian_entity.current = project_profile_json['backer_money']
        modian_entity.support_num = project_profile_json['backer_count']
        modian_entity.post_id = project_profile_json['moxi_post_id']
        modian_entity.title = project_profile_json['name']
        return modian_entity.target, modian_entity.current, modian_entity.title, modian_entity.support_num

    def query_project_orders(self, modian_entity, page=1, page_size=20):
        """
        查询项目订单（bs4版本）
        :param page_size:
        :param page:
        :param modian_entity:
        :return:
        """
        my_logger.info('查询项目订单, pro_id: %s', modian_entity.pro_id)
        api = 'https://zhongchou.modian.com/comment/ajax_comments?jsonpcallback=jQuery1_1&post_id={}&pro_class={}&page={}&page_size={}&_=2'.format(
            modian_entity.post_id,
            modian_entity.pro_class, page, page_size)
        r = self.session.get(api, headers=self.modian_header()).text
        r = r[40: -2]
        order_html = json.loads(r, encoding='utf-8')['html']
        soup = BeautifulSoup(order_html, 'lxml')
        # print(soup.prettify())
        # 对评论列表进行处理
        comment_list = soup.find_all(name='li')
        return comment_list

    def get_all_orders(self, modian_entity):
        """
        获取全部订单
        :return:
        """
        orders = []
        page = 1
        while True:
            my_logger.debug('获取全部订单，第{}页'.format(page))
            sub_orders = self.query_project_orders(modian_entity, page)
            # TODO: 这里需要处理
            if len(sub_orders) > 0:
                orders.extend(sub_orders)
                page += 1
            else:
                break
        return orders

    def modian_header(self):
        """
        微打赏header信息
        """
        header = {
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Host': 'zhongchou.modian.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.40',
        }
        return header


if __name__ == '__main__':
    entity_array = []
    entity1 = ModianEntity('http://www.baidu.com', 'test', 79264)
    entity_array.append(entity1)
    handler = ModianHandlerBS4(['483548995'], entity_array)
    handler.get_project_profiles(entity1)
    rst = handler.get_all_orders(entity1)
    print(rst)
