from django.db import connections
from utils import utils


class CardDrawLine:
    def __init__(self, supporter_id, supporter_name, card_num):
        self.supporter_id = supporter_id
        self.supporter_name = supporter_name
        self.card_num = card_num


class CardDrawHandler:
    def get_draw_record_by_supporter(self):
        with connections['modian'].cursor() as cursor:
            cursor.execute("""
            select s.`id` as supporter_id, s.`name` as supporter_name, c.`id` as card_id, c.`name` as card_name, count(*) as c
                from  supporter s, card c , draw_record dr 
                where s.`id` = dr.`supporter_id` and c.`id` = dr.`card_id`
                group by c.id, s.id
                order by s.id, c.id;
            """)
            draw_record_list = utils.namedtuplefetchall(cursor)

        tmp = {}
        for result in draw_record_list:
            s_id = result.supporter_id
            if s_id not in tmp:
                tmp[s_id] = {}
                tmp[s_id]['supporter_name'] = result.supporter_name
                tmp[s_id]['cards'] = {}
            c_id = result.card_id
            c_name = result.card_name
            if c_id not in tmp[s_id]['cards']:
                tmp[s_id]['cards'][c_id] = {}
                tmp[s_id]['cards'][c_id]['name'] = c_name
                tmp[s_id]['cards'][c_id]['count'] = result.c

        return tmp

    def get_draw_fu_record_by_supporter(self):
        with connections['modian'].cursor() as cursor:
            cursor.execute("""
            select s.`id` as supporter_id, s.`name` as supporter_name, dr.`fu_idx` as fu_id, dr.`fu_name` as fu_name, count(*) as c
                from  supporter s, t_draw_fu_record dr 
                where s.`id` = dr.`modian_id`
                group by dr.`fu_idx`, s.id
                order by s.id, dr.`fu_idx`;
            """)
            draw_record_list = utils.namedtuplefetchall(cursor)

        tmp = {}
        for result in draw_record_list:
            s_id = result.supporter_id
            if s_id not in tmp:
                tmp[s_id] = {}
                tmp[s_id]['supporter_name'] = result.supporter_name
                tmp[s_id]['cards'] = {}
            c_id = result.fu_id
            c_name = result.fu_name
            if c_id not in tmp[s_id]['cards']:
                tmp[s_id]['cards'][c_id] = {}
                tmp[s_id]['cards'][c_id]['name'] = c_name
                tmp[s_id]['cards'][c_id]['count'] = result.c

        return tmp
