from modian.logic.modian_handler import *
from modian.logic.modian_handler_bs4 import *
from modian.logic.weixin_handler import *
from modian.logic.taoba_handler import *
import uuid
import logging
from django_exercise.mysql_util import mysql_util2 as mysql_util
from django_exercise import utils

logger = logging.getLogger(__name__)


def sync_order(pro_id):
    modian_handler = ModianHandler()
    orders = modian_handler.get_all_orders(pro_id)
    print('订单数: {}'.format(len(orders)))
    for order in orders:
        user_id = order['user_id']
        nickname = order['nickname']
        pay_time = order['pay_time']
        backer_money = order['backer_money']

        oid = uuid.uuid3(uuid.NAMESPACE_OID, str(user_id) + pay_time)

        rst = mysql_util.select("""
                select * from `order` where id='%s'
            """ % oid)
        if len(rst) == 0:
            print('该订单不在数据库中')
            print('oid: %s', oid)
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
            pass
            # print('该订单已经在数据库中')
    mysql_util.close()


def sync_order2(pro_id):
    entity_array = []
    entity1 = ModianEntity('http://www.baidu.com', 'test', pro_id)
    entity_array.append(entity1)
    handler = ModianHandlerBS4(['483548995'], entity_array)

    handler.get_project_profiles(entity1)

    orders = handler.get_all_orders(entity1)

    for comment in orders:
        user_id = comment.find(class_='comment-replay').get('data-reply_ruid')
        nickname = comment.find(class_='nickname').get_text().strip('\n')

        timeArray = time.localtime(time.time())
        pay_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        backer_money_icon = comment.find(class_='icon-payment')
        if not backer_money_icon:  # 纯评论，直接跳过
            continue
        backer_money = comment.find(class_='comment-txt').get_text().strip()[4:-1]
        backer_money = float(backer_money)
        comment_id = comment.get('data-reply-id')

        # oid使用项目id和评论id拼装
        oid = str(pro_id) + str(comment_id)
        my_logger.debug('oid: %s', oid)

        rst = mysql_util.select("""
                        select * from `order` where id='%s'
                    """ % oid)
        if len(rst) == 0:
            print('该订单不在数据库中')
            print('oid: %s', oid)
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
            pass
            # print('该订单已经在数据库中')
    mysql_util.close()


def sync_order3(pro_id):
    entity_array = []
    entity1 = GroupAccountEntity('http://www.baidu.com', 'test', pro_id)
    entity_array.append(entity1)
    handler = WeixinGroupAccountHandler(['483548995'], entity_array)

    # handler.get_project_profiles(entity1)

    orders = handler.get_all_orders(entity1)

    for order in orders:
        if 'remark' in order.keys():
            user_id = order['remark']
            nickname = order['remark']
        else:
            user_id = order['nickname']
            nickname = order['nickname']
        pay_time = order['time']
        backer_money = float(order['fee']) / 100
        listid = int(order['listid'])

        my_logger.debug('oid: %s', listid)
        print(listid)

        rst = mysql_util.select("""
                            select * from `order` where id='%s'
                        """ % listid)
        if len(rst) == 0:
            print('该订单不在数据库中')
            print('oid: %s' % listid)
            # 每次需要更新一下昵称
            # mysql_util.query("""
            #                                     INSERT INTO `supporter` (`id`, `name`) VALUES (%s, '%s')  ON DUPLICATE KEY
            #                                         UPDATE `name`='%s'
            #                                     """ % (user_id, nickname, nickname))
            mysql_util.query("""
                                INSERT INTO `order` (`id`, `supporter_id`, `backer_money`, `pay_time`, `pro_id`) VALUES
                                    ('%s', '%s', %s, '%s', '%s');
                            """ % (listid, user_id, backer_money, pay_time, pro_id))
        else:
            pass
            # print('该订单已经在数据库中')
    mysql_util.close()


def sync_order4(pro_id):
    """
    桃叭补充遗漏订单
    :param pro_id:
    :return:
    """
    entity_array = []
    entity1 = TaoBaEntity('http://www.baidu.com', 'test', pro_id)
    entity_array.append(entity1)
    handler = TaoBaAccountHandler(['483548995'], entity_array)

    # handler.get_project_profiles(entity1)

    orders = handler.get_all_orders(entity1)
    for order in orders:
        user_id = order['userid']
        nickname = order['nickname']
        pay_time = utils.convert_timestamp_to_timestr(order['addtime'] * 1000)

        single_price = order['amount']
        pay_amount = order['nums']

        backer_money = single_price
        listid = int(order['id'])

        my_logger.debug('oid: %s', listid)

        rst = mysql_util.select("""
                                    select * from `order` where id='%s'
                                """ % listid)
        if len(rst) == 0:
            print('该订单不在数据库中')
            print('oid: %s' % listid)
            # 每次需要更新一下昵称
            mysql_util.query("""
                                                    INSERT INTO `supporter` (`id`, `name`) VALUES (%s, %s)  ON DUPLICATE KEY
                                                        UPDATE `id`=%s
                                                    """, (user_id, nickname, user_id))
            mysql_util.query("""
                INSERT INTO `order` (`id`, `supporter_id`, `backer_money`, `pay_time`, `pro_id`) VALUES
                                            ('%s', '%s', %s, '%s', '%s');
                                    """ % (listid, user_id, backer_money, pay_time, pro_id))
        else:
            pass
            # print('该订单已经在数据库中')
    mysql_util.close()


if __name__ == '__main__':
    # 44611, 45584, 47645, 47863, 48285, 50755, 51567, 54590, 55194, 57085, 57083, 59267,
    # 59708, 61410, 62988, 64096, 64735, 65643, 66888, 68067,
    # 69304, 70158, 70956, 71842, 72535, 73894, 74791, 75412
    # sync_order2(79264)
    # sync_order3('4mr9Xz920100009000043331')
    sync_order4('1114')

