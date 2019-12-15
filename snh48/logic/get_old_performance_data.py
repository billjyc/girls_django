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
    soup = BeautifulSoup(r)
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
        ('http://snh48club.com/video/1236.html', 1552),  # 1004
        ('http://snh48club.com/video/1234.html', 1553),  # 1003
        ('http://snh48club.com/video/1222.html', 1556),  # 1002
        ('http://snh48club.com/video/1221.html', 1557),  # 0921
        ('http://snh48club.com/video/1213.html' , 1560),  # 0920
        ('http://snh48club.com/video/1202.html' , 1563),  # 0919
        # ('http://snh48club.com/video/1275.html', 1574),  # 0914
        # ('http://snh48club.com/video/1272.html' , 1577),  # 0913
        # ('http://snh48club.com/video/1271.html' , 1578),  # 0912
        # ('http://snh48club.com/video/1266.html', 1579),  # 0908
        # ('http://snh48club.com/video/1264.html', 1582),  # 0907
        # ('http://snh48club.com/video/1246.html', 1547),  # 0823
        # ('http://snh48club.com/video/1238.html' , 1550),  # 0817

    ]
    for performance in performance_list:
        get_performance_data(performance[0], performance[1])
