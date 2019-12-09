# -*- coding: utf-8 -*-
"""
从snh48club.com处获取参加公演成员的信息
"""
import logging
from django_exercise.mysql_util import mysql_util
from bs4 import BeautifulSoup
import requests


logger = logging.getLogger(__name__)

member_list_db = mysql_util.select("""
SELECT id, name from memberinfo;
""")
name_to_id_dict = {}
for member in member_list_db:
    name_to_id_dict[member[1]] = member[0]
print(name_to_id_dict)


def get_performance_data(performance_url, performance_id):
    """
    获取公演资料
    :param performance_url: snh48club.com的公演详情url
    :param performance_id: db中存放的公演记录id
    :return:
    """
    r = requests.get(performance_url).text.replace('\n', '').replace('\r', '')
    soup = BeautifulSoup(r, 'lxml')
    member_list = soup.find(id='spanMember')
    sql = """
    INSERT INTO `member_performance_history` (`member_id`, `performance_history_id`)
            VALUES """
    for member in member_list:
        if member.name and member.name != 'h3':
            sql += "({}, {}),".format(name_to_id_dict[member.get_text()], performance_id)
    sql = sql[:-1]
    print(sql)
    mysql_util.query(sql)


if __name__ == '__main__':
    performance_list = [
        ('http://snh48club.com/video/8955.html', 1969),
        ('http://snh48club.com/video/8951.html', 1975),
        ('http://snh48club.com/video/8936.html', 1977),
        ('http://snh48club.com/video/8931.html', 1938),
        ('http://snh48club.com/video/8906.html' , 1943),
        ('http://snh48club.com/video/8900.html' , 1948),
        ('http://snh48club.com/video/8894.html' , 1954),
        ('http://snh48club.com/video/9017.html' , 1960),
        ('http://snh48club.com/video/8978.html' , 1961),
        ('http://snh48club.com/video/10215.html' , 1922),
        ('http://snh48club.com/video/10205.html' , 1923),
        ('http://snh48club.com/video/10157.html' , 1928),
        ('http://snh48club.com/video/10136.html', 1930),
        ('http://snh48club.com/video/8954.html', 1932),

    ]
    for performance in performance_list:
        get_performance_data(performance[0], performance[1])
