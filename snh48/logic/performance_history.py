# -*- coding: utf-8 -*-
"""
从snh48的售票记录中爬取公演信息
"""
import logging

import pymysql
import requests
import time
import json

logger = logging.getLogger(__name__)


years = ['2013', '2014', '2015', '2016']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']


def get_performance_history():
    conn = pymysql.connect(host='localhost', port=3306, passwd='123456', db='snh48', user='root', charset='utf8')
    cursor = conn.cursor()
    for year in years:
        for month in months:
            if year == '2013' and month in ['01', '02', '03', '04', '05', '06', '07']:
                continue
            date_str = year + '-' + month
            print(date_str)
            url = 'http://www.snh48.com/ticketsinfo.php?act=choose'
            header = {
                'Host': 'www.snh48.com',
                'Referer': 'http://www.snh48.com/ticket.php',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }
            param = {
                'date': date_str,
                'team': 0,
            }
            r = requests.post(url, headers=header, params=param).json()

            for history in r:
                print(history['title'])
                try:
                    cursor.execute("""
                        insert into `performance_history` (`performance_id`, `date`, `description`) VALUES 
                         (%s, '%s', '%s');
                    """ % (0, history['addtime'], history['special']))
                    conn.commit()
                except pymysql.Error as e:
                    conn.rollback()
                    logger.error('连接mysql出现错误: %s', e)
    conn.close()


def get_performance_history_new(gid, date_str):
    conn = pymysql.connect(host='localhost', port=3306, passwd='****', db='snh48', user='root', charset='utf8')
    cursor = conn.cursor()
    time0 = int(time.time() * 1000)

    url = 'https://api.snh48.com/getticketinfo.php?gid={}&callback=jQuery1111042178951578927815_1580971010393&act=choose&date={}&team=ALL&_={}'.format(gid, date_str, time0)
    header = {
        'Host': 'api.snh48.com',
        'Referer': 'http://www.snh48.com/ticket.php',
    }
    param = {
        'date': date_str,
        'team': 'ALL',
        'gid': gid,
        'act': 'choose',
        'callback': 'jQuery1111042178951578927815_1580971010393',
        '_': time0
    }
    r = requests.get(url, headers=header).text
    prefix_len = len('jQuery1111042178951578927815_1580971010393')
    r = r[prefix_len + 2: -1]
    r = json.loads(r, encoding='utf-8')
    for history in r['desc']:
        print(history)
        try:
            cursor.execute("""
                    insert into `performance_history` (`performance_id`, `date`, `description`) VALUES
                     (%s, '%s', '%s');
                """ % (0, history['date'], history['bz']))
            conn.commit()
        except pymysql.Error as e:
            conn.rollback()
            logger.error('连接mysql出现错误: %s', e)
    conn.close()


if __name__ == '__main__':
    # get_performance_history()
    get_performance_history_new(2, '2020-01')
    get_performance_history_new(1, '2020-01')
    get_performance_history_new(3, '2020-01')
