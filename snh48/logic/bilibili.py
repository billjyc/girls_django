import requests
import logging
import pymysql
from django_exercise import utils
import time

logger = logging.getLogger(__name__)


def get_video_stat(aid):
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=%s' % aid
    header = {
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Referer': 'https://www.bilibili.com/video/av%s' % aid,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=header).json()
        return r['data']
    except Exception as e:
        logger.error(e)
    return None


def get_aid_from_link(link):
    strs = link.split('av')
    return strs[1]


try:
    conn = pymysql.connect(host='root', port=3306, passwd='Jyc@1993', db='snh48', user='root', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("""
        select id, video_url from performance_history where video_url is not null
    """)
    rst = cursor.fetchall()
    for (id, video_url) in rst:
        aid = get_aid_from_link(video_url)
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
    conn.close()

except pymysql.Error as e:
    conn.rollback()
    logger.error('连接mysql出现错误: %s', e)


if __name__ == '__main__':
    pass
    # aid = get_aid_from_link('https://www.bilibili.com/video/av22103177')
    # r = get_video_stat(19424846)
    # print(r)
