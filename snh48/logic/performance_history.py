# -*- coding: utf-8 -*-
"""
从snh48的售票记录中爬取公演信息
"""
import logging

import pymysql
import requests

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


if __name__ == '__main__':
    get_performance_history()
