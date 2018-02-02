# -*- coding:utf-8 -*-
"""
摩点API文档地址：https://www.showdoc.cc/1702718?page_id=15700669
"""
import sys

import requests

import time
import hashlib
import urllib
import util


class ModianEntity:
    def __init__(self, link, title, pro_id, need_display_rank=False, current=0.0, target=0.0, support_num=0):
        self.link = link
        self.title = title
        self.pro_id = pro_id
        self.need_display_rank = need_display_rank
        self.current = current
        self.target = target
        self.support_num = support_num


class ModianHandler:
    def __init__(self):
        self.session = requests.session()

    def modian_header(self):
        """
        微打赏header信息
        """
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.40',
        }
        return header

    def get_all_orders(self, pro_id):
        """
        获取全部订单
        :return:
        """
        orders = []
        page = 1
        while True:
            sub_orders = self.query_project_orders(pro_id, page)
            if len(sub_orders) > 0:
                orders.extend(sub_orders)
                page += 1
            else:
                break
        return orders

    def query_project_orders(self, pro_id, page=1):
        """
        查询项目订单（摩点API版本）
        :param page:
        :param modian_entity:
        :return:
        """
        api = 'https://wds.modian.com/api/project/orders'
        params = {
            'pro_id': pro_id,
            'page': page
        }
        r = requests.post(api, self.make_post_params(params), headers=self.modian_header()).json()
        if int(r['status']) == 0:
            orders = r['data']
            return orders
        else:
            raise RuntimeError('获取项目订单查询失败')

    def make_post_params(self, post_fields):
        """
        获取post请求需要的参数
        :param post_fields:
        :return:
        """
        sign = self.__make_signature(post_fields)
        post_fields['sign'] = sign
        return post_fields

    def __make_signature(self, post_fields):
        """
        生成调用微打赏接口所需的签名

        PHP的例子：
            $post_fields = $_POST;
            ksort($post_fields);
            $md5_string = http_build_query($post_fields);
            $sign = substr(md5($md5_string), 5, 21);

        :param post_fields: post请求的参数
        :return:
        """
        post_fields_sorted = util.ksort(post_fields)
        md5_string = urllib.urlencode(post_fields_sorted) + '&p=das41aq6'
        sign = hashlib.md5(md5_string.encode('utf-8')).hexdigest()[5:21]
        return sign


if __name__ == '__main__':
    pass
