# -*- coding: utf-8 -*-
import time
import random
import urllib.parse
import hashlib
import requests
from collections import namedtuple


def convert_timestamp_to_timestr(timestamp):
    """
    将13位时间戳转换为字符串
    :param timestamp:
    :return:
    """
    timeArray = time.localtime(timestamp / 1000)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return time_str


def convert_timestr_to_timestamp(time_str):
    """
    将时间字符串转换为时间戳
    :param time_str:
    :return:
    """
    timestamp = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    return timestamp


def random_str(strs):
    return random.choice(strs)


def make_signature(post_fields):
    """
    生成调用微打赏接口所需的签名

    PHP的例子：
        $post_fields = $_POST;
        ksort($post_fields);
        $md5_string = http_build_query($post_fields);
        $sign = substr(md5($md5_string), 5, 16);

    :param post_fields: post请求的参数
    :return:
    """
    post_fields_sorted = ksort(post_fields)
    md5_string = urllib.parse.urlencode(post_fields_sorted) + '&p=das41aq6'
    # print md5_string
    sign = hashlib.md5(md5_string).hexdigest()[5:21]
    # print sign
    return sign


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class TransferType:
    DEBUT = 1  # 出道
    TRANSFER = 2  # 移籍
    DELEGATE = 3  # 降格
    PROMOTE = 4  # 升格
    CONCURRENT_START = 5  # 兼任开始
    CONCURRENT_END = 6  # 兼任解除
    RETIRE = 7  # 退团
    COMEBACK = 8  # 回归
    GRADUATE = 9  # 毕业
    STAR_PALACE = 10  # 明星殿堂


def process_transfer_detail(transfer_detail, team_dict):
    transfer_type = transfer_detail['type']
    to_team_name = ''
    if transfer_detail["to_team"]:
        to_team_name = team_dict[str(transfer_detail["to_team"])]
    description = ""
    if transfer_type == TransferType.DEBUT:
        description += "出道, "
        description += "加入{}".format(transfer_detail["batch"])
        if to_team_name:
            description += "& {}".format(to_team_name)
    elif transfer_type == TransferType.TRANSFER:
        description += "移籍至{}".format(to_team_name)
    elif transfer_type == TransferType.DELEGATE:
        description += "降格至{}".format(to_team_name)
    elif transfer_type == TransferType.PROMOTE:
        description += "升格至{}".format(to_team_name)
    elif transfer_type == TransferType.CONCURRENT_START:
        description += "兼任{}".format(to_team_name)
    elif transfer_type == TransferType.CONCURRENT_END:
        description += "{}兼任解除".format(to_team_name)
    elif transfer_type == TransferType.RETIRE:
        description += "停止活动"
    elif transfer_type == TransferType.COMEBACK:
        description += "回归, 加入{}".format(to_team_name)
    elif transfer_type == TransferType.GRADUATE:
        description += "毕业"
    elif transfer_type == TransferType.STAR_PALACE:
        description += "升入明星殿堂"
    return description


if __name__ == '__main__':
    # strs = filter_tags("""
    # test<span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_tu-65768ccc23.png\" style=\"width:1em;height:1em;\" alt=\"[吐]\"></span><span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_haha-bdd6ceb619.png\" style=\"width:1em;height:1em;\" alt=\"[哈哈]\"></span><span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_tu-65768ccc23.png\" style=\"width:1em;height:1em;\" alt=\"[吐]\"></span><span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/others/l_xin-8e9a1a0346.png\" style=\"width:1em;height:1em;\" alt=\"[心]\"></span><br/><a class='k' href='https://m.weibo.cn/k/test?from=feed'>#test#</a>
    # """)
    # print strs
    url = 'https://wds.modian.com/api/project/orders'
    post_fields = {
        "pro_id": 10289,
        "page": 1,
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4033.400 QQBrowser/9.7.12622.400'}
    sign = make_signature(post_fields)
    post_fields['sign'] = sign

    r = requests.post(url, post_fields, headers=header)
    # print r.text
