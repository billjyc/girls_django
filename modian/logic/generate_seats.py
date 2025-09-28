# -*- coding:utf-8 -*-
"""
根据号码算出座位号，并生成excel文件
"""

import logging

import xlwt

from utils.mysql_util import mysql_util2 as mysql_util

logger = logging.getLogger(__name__)


rst = mysql_util.select("""
    SELECT s.name, (sr.`seats_number` - 1) DIV 30 + 1, (sr.`seats_number`) % 30
FROM `seats_record` sr, `supporter` s 
where s.`id`=sr.`modian_id` and sr.`seats_type`=1 order by s.`id`, sr.`seats_number`; 
""")

seats_dict = {}

for item in rst:
    if item[0] not in seats_dict.keys():
        seats_dict[item[0]] = []
    seats = '{}.{}'.format(item[1], item[2])
    seats_dict[item[0]].append(seats)
print(seats_dict)


wbk = xlwt.Workbook(encoding='utf-8')
sheet = wbk.add_sheet('Sheet1')
row0 = [u'摩点昵称', u'抽选结果']
for i in range(len(row0)):
    sheet.write(0, i, row0[i])

cur_row = 1
for k, v in seats_dict.items():
    sheet.write(cur_row, 0, k)
    for j in range(len(v)):
        sheet.write(cur_row, j + 1, v[j])
    cur_row += 1
wbk.save('座位统计.xls')



