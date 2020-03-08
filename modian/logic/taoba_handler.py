# -*- coding:utf-8 -*-
"""
微信小经费
"""

import json
import logging
import time
import zlib
import base64

import requests


my_logger = logging.getLogger(__name__)


class TaoBaEntity:
    def __init__(self, link, title, taoba_id, broadcast_groups=[], qrcode='', current=0.0, support_num=0):
        self.link = link
        self.title = title
        self.taoba_id = taoba_id
        # self.need_display_rank = need_display_rank
        self.broadcast_groups = broadcast_groups
        self.qrcode = qrcode
        self.current = current
        # self.target = target
        self.support_num = support_num


class TaoBaAccountHandler:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, taoba_notify_groups, taoba_project_array):
        self.session = requests.session()
        self.taoba_notify_groups = taoba_notify_groups
        self.taoba_project_array = taoba_project_array

        # self.card_draw_handler = card_draw_handler
        self.order_queues = {}
        self.token = 0

    def init_order_queues(self):
        for taoba_entity in self.taoba_project_array:
            try:
                my_logger.info('初始化%s的订单队列', taoba_entity.taoba_id)
                my_logger.debug(self.order_queues)
                if taoba_entity.taoba_id not in self.order_queues:
                    self.order_queues[taoba_entity.taoba_id] = set()
                    my_logger.debug('队列为空，重新初始化队列')
                else:
                    my_logger.debug('队列不为空，不重新初始化队列')
                    continue
                my_logger.debug('项目%s队列长度: %s', taoba_entity.taoba_id,
                                len(self.order_queues[taoba_entity.taoba_id]))

                orders = self.query_project_orders(taoba_entity)

                for order in orders:
                    listid = int(order['id'])
                    self.order_queues[taoba_entity.taoba_id].add(listid)
            except Exception as e:
                my_logger.error('初始化订单队列失败！')
                my_logger.exception(e)

    def taoba_header(self):
        """
        header信息
        """
        header = {
            'Content-Type': 'application/json',
            'SIGNATURE': '3130313531323438247b226964223a31303135313234382c225f223a313538333637363034387d6ce2c12a3308',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        }
        return header

    def query_project_orders(self, taoba_entity, page=1, request_time=int(time.time() * 1000)):
        """
        批量获取订单
        :param taoba_entity:
        :param page:
        :param request_time:
        :return:
        """
        my_logger.info('查询项目订单, id: %s', taoba_entity.taoba_id)
        url = 'https://www.tao-ba.club/idols/refund/orders'
        data = {'id': taoba_entity.taoba_id, 'offset': 0, 'ismore': False, 'requestTime': request_time,
                'pf': 'h5'}
        r = self.session.post(url=url, data=self.encrypt(data), headers=self.taoba_header())
        r = self.decrypt(r.text)
        if int(r['code']) != 0:
            raise RuntimeError('获取订单信息失败')
        orders = r['list']
        my_logger.info('项目订单: page: %s, orders: %s', page, orders)
        return orders

    def get_current_and_target(self, taoba_entity):
        """
        查询当前项目情况
        :param taoba_entity:
        :return:
        """
        my_logger.info('获取当前进度和总额: pro_id: %s', taoba_entity.taoba_id)
        api = 'https://www.tao-ba.club/idols/detail'
        data = {'id': taoba_entity.taoba_id, 'requestTime': int(time.time() * 1000), 'pf': 'h5'}
        r = self.session.post(api, data=self.encrypt(data), headers=self.taoba_header())
        r = self.decrypt(r.text)
        if int(r['code']) == 0:
            name = r['datas']['title']
            current = r['datas']['donation']
            # user_num = r['user_num']
            user_num = 0
            my_logger.info('支持人数: %s, 当前进度: %s', user_num, current)
            return name, current, user_num
        else:
            raise RuntimeError('获取项目筹款结果查询失败')

    def get_all_orders(self, taoba_entity):
        orders = []
        request_time = int(time.time() * 1000)
        sub_orders = self.query_project_orders(taoba_entity, request_time)
        orders.extend(sub_orders)
        # while True:
        #     sub_orders = self.query_project_orders(taoba_entity, request_time)
        #     if sub_orders:
        #         print(sub_orders)
        #         print(request_time)
        #         orders.extend(sub_orders)
        #
        #         for order in sub_orders:
        #             request_time = request_time if order['addtime'] * 1000 >= request_time else order['addtime'] * 1000
        #     else:
        #         break
        return orders

    def decrypt(self, response):
        """
        对加密的response进行解密
        :return:
        """
        my_logger.info('对加密的response进行解密')
        my_logger.info('1. 分离出base64字符串')
        response_arr = response.split('$', 2)
        if len(response_arr) < 2:
            raise RuntimeError('response格式错误')
        base64_res = response_arr[1]
        my_logger.info('2. base64解码')
        base64_res = base64.b64decode(base64_res)
        my_logger.info('3. 对字符串进行进一步处理')
        res = self.process(base64_res)
        my_logger.info('4. 对处理结果进行zlib解压缩')
        res = zlib.decompress(res)
        return json.loads(str(res, encoding='utf-8'))

    def encrypt(self, request):
        """
        对request进行加密
        :param request:
        :return:
        """
        my_logger.info('对request进行加密')
        my_logger.info('1. 对字符串进行zlib压缩')
        res_str = json.dumps(request).strip()
        res = zlib.compress(bytes(res_str, encoding='utf-8'))
        my_logger.info('2. 对字符串进行处理')
        res = self.process(res)
        my_logger.info('3. base64编码')
        res = base64.b64encode(res)
        my_logger.info('4. 组装字符串')
        res = str(len(res_str)) + '$' + str(res, encoding='utf-8')
        return res

    def process(self, byte_str):
        """
        桃叭对字符串独有的处理函数
        :param byte_str:
        :return:
        """
        o = "%#54$^%&SDF^A*52#@7"
        n = bytes(o * 3, encoding='utf-8')
        t = b""
        i = 0
        for l in range(len(byte_str)):
            a = byte_str[l]
            if l % 2 == 0:
                index = i % len(o)
                a ^= n[index]
                i += 1
            t += a.to_bytes(length=1, signed=False, byteorder='big')
        return t

    def login(self, account, passwd):
        """
        登录，获取SIGNATURE
        :param account:
        :param passwd:
        :return:
        """
        url = 'https://www.tao-ba.club/signin/phone'
        data = {'account': account, 'pushid': '', 'loginpw': passwd,
                'device': {'platform': 'other', 'screen': '1680*1050', 'imei': 'XXX', 'uuid': 'YYY',
                           'version': 'v1.0.0', 'vendor': 'ZZZ'}, 'requestTime': int(time.time() * 1000), 'pf': 'h5'}
        header = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        }
        r = self.session.post(url, data=self.encrypt(data), headers=header)
        r = self.decrypt(r.text)
        if r['code'] == 0:
            my_logger.debug('登录成功')
            self.token = r['token']


if __name__ == "__main__":
    entity = TaoBaEntity('ssss', '400场', '1114')
    handler = TaoBaAccountHandler([], [entity])
    handler.get_all_orders(entity)
    # print(handler.decrypt(
    #     '209$XZw+jnQOtzAoBKHiRoV2TEcI+KNB4NiCaJEKoTyhNcT8a/h5UFcGnxMY1pPvoSWUy9Q/q4QWw8HS4ipHmHxu/kndw+OCWOQYRVa7Rx+sAmh72KJhu3wGecT3vwLE0UAiMWsVLR8o/i2AK2tGTtsySN7xUl3k4ZUQmb/TB7giMg9Uo1xMvr7BK91AnkRbf4YEKFR5KtRFakpw8JQT2mYx1ztGaTy4'))
    # print(handler.decrypt(
    #     '111$XZxGyR4OtDA0BZ67iUaS76Z/37JrhtoaXeHENDGHKjW06ChdvVnBHFg/kQgZzcAnjjHkxTMIajjE9fEKpu1az26+8rmrIZWgXWpKqlCl/w/uyC6Z'))
    # print(handler.decrypt('1059$XZyWkApP9zA0xeHL6AG77aC/KExmJAY6cRAskw1q5jYujX1UYr8elwFAYCVgAXlOKU/ze1i/TtSvJgSJWyz6MWv5iYOcgXF6UpY9yEbcb7d1obEkc8DGQu8jDQX/Nwncyj3KcL4geyIf1PAJ93SzNBWRoAJxl6PsO1XyIupVE68Mfh1pyFY6WCo8NNTWKB/ej6lulR1D8w5m2IXtJQ+9YZHOI/p9mwB1+EmSTpcUk9+su1DRskm32cAd+auY2GaScK2pMgixhlrA1K/AP90Lzye9zs3fRN5XecFI8f/Cit/xUH+zRP7cLNGPGISfIFWJ24ijddXUXSxioeLt1+hiXrsFbAtYysMjuHhx2YFFQ22lo5mWsurOQMG0ROYz7XPhrjb+bNHT057Cb+5ftu9XIBbj'))
    #
    # print(handler.decrypt('61$XZyIVv/J+M0IUewyF9B3yhxLb05Dst/M49To0uHioJDv3BQlHEN2C0ATBgM/I1dDLUs4paQ0divhDBWlBAAHXDup'))
    # print(handler.encrypt({'limit': 20, 'offset': 0, 'requestTime': 1583460827179, 'pf': 'h5'}))
    #
    # print(handler.decrypt('108$XZw2iQwStDAoA6Hiv0JviGre1gakmNShIVIb/CjRWlaYj5TLrawsQDvkiQ9tpVCdvFZfdob0VoHocWDPLvtquBNuVOD7jWKrJeaDTynJl/TkW5SHHs02LsoHnohzZA=='))
