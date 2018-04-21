from modian.logic.modian_handler import *
import uuid
import logging
from django_exercise.mysql_util import MySQLUtil

logger = logging.getLogger(__name__)
mysql_util = MySQLUtil('localhost', 3306, 'root', 'Jyc@1993', 'card_draw')


def sync_order(pro_id):
    modian_handler = ModianHandler()
    orders = modian_handler.get_all_orders(pro_id)
    for order in orders:
        user_id = order['user_id']
        nickname = order['nickname']
        pay_time = order['pay_time']
        backer_money = order['backer_money']

        oid = uuid.uuid3(uuid.NAMESPACE_OID, str(user_id) + pay_time)
        print('oid: %s', oid)

        rst = mysql_util.select("""
                select * from `order` where id='%s'
            """ % oid)
        if len(rst) == 0:
            print('该订单不在数据库中')
            # 每次需要更新一下昵称
            mysql_util.query("""
                                    INSERT INTO `supporter` (`id`, `name`) VALUES (%s, '%s')  ON DUPLICATE KEY
                                        UPDATE `name`='%s'
                                    """ % (user_id, nickname, nickname))
            mysql_util.query("""
                    INSERT INTO `order` (`id`, `supporter_id`, `backer_money`, `pay_time`, `pro_id`) VALUES 
                        ('%s', %s, %s, '%s', %s);
                """ % (oid, user_id, backer_money, pay_time, pro_id))
        else:
            print('该订单已经在数据库中')


if __name__ == '__main__':
    sync_order(13566)

