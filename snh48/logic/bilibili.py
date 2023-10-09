# -*- coding: utf-8 -*-
"""
根据公演av号获取B站视频播放量，弹幕数等信息
@Author: billjyc
"""

import requests
import logging
import pymysql
from django_exercise import utils
from django_exercise import db_config as Config
import time

logger = logging.getLogger(__name__)

def get_video_stat_new(bid):
    url = "https://api.bilibili.com/x/web-interface/view?bvid=%s" % bid
    header = {
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Referer': 'https://www.bilibili.com/video/BV%s' % bid,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=header).json()
        return r['data']['stat']
    except Exception as e:
        logger.error(e)
    return None


def get_video_stat(aid):
    url = 'https://api.bilibili.com/x/web-interface/view?aid=%s' % aid
    header = {
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Referer': 'https://www.bilibili.com/video/av%s' % aid,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=header).json()
        return r['data']['stat']
    except Exception as e:
        logger.error(e)
    return None


def get_aid_from_bid(bid):
    """
    从bid获取aid
    :param bid:
    :return:
    """
    logger.info('1.获取cid')
    url = 'https://api.bilibili.com/x/player/pagelist?bvid=%s&jsonp=jsonp' % bid
    header = {
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Referer': 'https://www.bilibili.com/video/bv%s' % bid,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=header).json()
        if r['code'] == 0:
            cid = r['data'][0]['cid']

            logger.info('2.获取aid')
            url2 = 'https://api.bilibili.com/x/web-interface/view?cid=%s&bvid=BV%s' % (cid, bid)
            r2 = requests.get(url2, headers=header).json()
            if r2['code'] == 0:
                return r2['data']['aid']
    except Exception as e:
        logger.exception(e)
    return None


def get_aid_from_link(link):
    strs = link.split('/')
    if 'av' in strs[4]:
        return strs[4].split('av')[1]
    else:
        # return strs[4].split('BV')[1]
        return get_aid_from_bid(strs[4].split('BV')[1])


try:
    conn = pymysql.connect(host=Config.DB_HOST, port=Config.DB_PORT, passwd=Config.DB_PASSWORD, db='snh48',
                           user=Config.DB_USER, charset=Config.DB_CHARSET)
    cursor = conn.cursor()
    cursor.execute("""
        select id, video_url from performance_history where video_url is not null order by date desc
    """)
    rst = cursor.fetchall()
    for (id, video_url) in rst:
        if not video_url:
            continue
        aid = get_aid_from_link(video_url)
        print(aid)
        if not aid:
            continue

        datas = get_video_stat(aid)

        print(datas)
        cursor.execute("""
            select * from bilibili_stat where performance_history_id=%s
        """ % (id, ))
        stat = cursor.fetchall()
        time_str = utils.convert_timestamp_to_timestr(time.time() * 1000)
        if len(stat) == 0:
            cursor.execute("""
                INSERT INTO bilibili_stat (performance_history_id, aid, view, danmaku, reply, favorite, coin, share, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '%s')
            """ % (id, aid, datas['view'], datas['danmaku'], datas['reply'], datas['favorite'], datas['coin'], datas['share'], time_str))
        else:
            cursor.execute("""
                UPDATE bilibili_stat SET view=%s,danmaku=%s,reply=%s,favorite=%s,coin=%s,share=%s, update_time='%s' WHERE performance_history_id=%s
            """ % (datas['view'], datas['danmaku'], datas['reply'], datas['favorite'], datas['coin'], datas['share'], time_str, id))
        conn.commit()
        time.sleep(2)
    conn.close()

except pymysql.Error as e:
    conn.rollback()
    logger.error('连接mysql出现错误: %s', e)


if __name__ == '__main__':
    pass
