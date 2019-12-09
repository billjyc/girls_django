# -*- coding: utf-8 -*-

import pymysql
import logging
from django_exercise import db_config as Config
logger = logging.getLogger('django')


class MySQLUtil:
    def __init__(self, host, port, user, passwd, db):
        self.conn = self.getConn(host, port, user, passwd, db)

    def getConn(self, host, port, user, passwd, db, charset="utf8"):
        logger.debug('获取数据库连接')
        try:
            conn = pymysql.connect(host=host, port=port, passwd=passwd, db=db, user=user, charset=charset)
            return conn
        except pymysql.Error as e:
            logger.exception('连接mysql出现错误: %s', e)

    def select(self, sql):
        logger.info('查询: %s', sql)
        cursor = self.conn.cursor()
        data = None
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
        except pymysql.Error as e:
            logger.exception('数据库select出现错误: %s', e)
        finally:
            cursor.close()
        return data

    def query(self, sql):
        """
        插入，删除，更新操作
        :param sql:
        :return:
        """
        logger.info('mysql语句: %s', sql)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except pymysql.Error as e:
            logger.exception('数据库操作出现错误: %s', e)
            self.conn.rollback()
        finally:
            cursor.close()

    def close(self):
        self.conn.close()


mysql_util = MySQLUtil(Config.DB_HOST, Config.DB_PORT, Config.DB_USER, Config.DB_PASSWORD, 'snh48')
mysql_util2 = MySQLUtil(Config.DB_HOST, Config.DB_PORT, Config.DB_USER, Config.DB_PASSWORD, 'card_draw')


if __name__ == '__main__':
    pass



