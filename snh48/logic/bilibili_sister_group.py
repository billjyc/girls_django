# -*- coding: utf-8 -*-
import requests
import logging
import pymysql
from django_exercise import utils
import time
import csv

logger = logging.getLogger(__name__)


def get_video_stat(keyword):
    print(keyword)
    page = 1
    result = []
    while True:
        url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=1315101&pagesize=100&tid=0&page=%s&keyword=%s&order=pubdate' % (page, keyword)
        header = {
            'Host': 'space.bilibili.com',
            'Referer': 'https://space.bilibili.com/1315101/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        r = requests.get(url, headers=header).json()
        vlist = r['data']['vlist']
        if len(vlist) == 0:
            break
        print(vlist)
        result.extend(vlist)
        page += 1
        time.sleep(5)

    # 写入csv文件
    with open('%s.csv' % keyword, 'w', encoding='utf8') as f:
        writer = csv.writer(f, dialect=('excel'))
        writer.writerow(['上传时间', '公演', '播放量', '弹幕'])
        for video in result:
            if '生日会' in video['title']:
                continue
            # 转换成localtime
            time_local = time.localtime(video['created'])
            # 转换成新的时间格式(2016-05-05 20:28:54)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

            writer.writerow([dt, video['title'], video['play'], video['video_review']])


if __name__ == '__main__':
    # get_video_stat('Team NII')
    # get_video_stat('Team HII')
    # get_video_stat('Team X')
    # get_video_stat('Team XII')
    # get_video_stat('Team B')
    # get_video_stat('Team E')
    # get_video_stat('Team J')
    # get_video_stat('Team G')
    # get_video_stat('Team NIII')
    get_video_stat('Team Z')
