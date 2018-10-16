# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render

from .logic.modian_handler import ModianHandler
from .logic.card_draw_handler import CardDrawHandler
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .logic.birthday_form import BirthdayForm
import logging
from django.http import HttpResponse
import json
from django_exercise import utils
from django.core import serializers
from django.db.models import Count
from django.db import connections


logger = logging.getLogger('django')


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the logic index.")


def get_all_orders(request, pro_id):
    # modian_handler = ModianHandler()
    page = request.GET.get('page', 1)
    logger.debug('page: %s', page)
    order_list = Order.objects.filter(pro_id=pro_id).order_by('-pay_time')
    logger.debug('order list: %s', order_list)
    paginator = Paginator(order_list, 20)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {
        'orders': orders,
    }
    return render(request, 'modian/orders.html', context)


def get_all_card_draw_record(request):
    records = DrawRecord.objects.order_by('-draw_time')
    context = {
        'records': records,
    }
    return render(request, 'modian/draw-records.html', context)


def get_card_draw_record_by_supporter(request):
    handler = CardDrawHandler()
    records = handler.get_draw_record_by_supporter()
    cards = Card.objects.order_by('id')
    context = {
        'records': records,
        'cards': cards,
    }
    return render(request, 'modian/draw-records-statistics.html', context)


def get_300_activity_detail(request):
    seat_records = SeatsRecord.objects.filter(seats_type=1).order_by('seats_number')
    standing_records = SeatsRecord.objects.filter(seats_type=2).order_by('seats_number')

    for seat in seat_records:
        seat.row = int((seat.seats_number - 1) / 30) + 1
        seat.col = int((seat.seats_number - 1) % 30) + 1

    context = {
        'seat_records': seat_records,
        'standing_records': standing_records,
    }
    return render(request, 'modian/300-activity.html', context)


def get_61_pk_detail(request):
    from .logic import modian_pk_handler
    fxf_basic_points = modian_pk_handler.get_basic_points(modian_pk_handler.FXF_PRO_ID)
    wjl_basic_points = modian_pk_handler.get_basic_points(modian_pk_handler.WJL_PRO_ID)

    fxf_make_trouble_times = modian_pk_handler.get_make_trouble_time(modian_pk_handler.FXF_PRO_ID)
    wjl_make_trouble_times = modian_pk_handler.get_make_trouble_time(modian_pk_handler.WJL_PRO_ID)

    fxf_make_plus_10_times = modian_pk_handler.get_plus_10_times(modian_pk_handler.FXF_PRO_ID)
    wjl_make_plus_10_times = modian_pk_handler.get_plus_10_times(modian_pk_handler.WJL_PRO_ID)

    fxf_bonus_minus_points = int(wjl_make_plus_10_times // 5) * 10
    wjl_bonus_minus_points = int(fxf_make_plus_10_times // 5) * 10

    fxf_make_trouble_points = int(fxf_make_trouble_times // 5) * 10
    wjl_make_trouble_points = int(wjl_make_trouble_times // 5) * 10

    fxf_make_trouble_minus_points = wjl_make_trouble_times * modian_pk_handler.WJL_MAKE_TROUBLE_POINTS
    wjl_make_trouble_minus_points = fxf_make_trouble_times * modian_pk_handler.FXF_MAKE_TROUBLE_POINTS

    fxf_supporter_num = modian_pk_handler.get_current_supporter_num(modian_pk_handler.FXF_PRO_ID)
    wjl_supporter_num = modian_pk_handler.get_current_supporter_num(modian_pk_handler.WJL_PRO_ID)

    fxf_supporter_points = 0
    wjl_supporter_points = 0
    if fxf_supporter_num > wjl_supporter_num:
        fxf_supporter_points = 61
    elif fxf_supporter_num < wjl_supporter_num:
        wjl_supporter_points = 61

    fxf_points = fxf_basic_points + fxf_make_trouble_points - fxf_bonus_minus_points - fxf_make_trouble_minus_points
    wjl_points = wjl_basic_points + wjl_make_trouble_points - wjl_bonus_minus_points - wjl_make_trouble_minus_points
    fxf_total_points = fxf_basic_points + fxf_make_trouble_points - fxf_bonus_minus_points - fxf_make_trouble_minus_points + fxf_supporter_points
    wjl_total_points = wjl_basic_points + wjl_make_trouble_points - wjl_bonus_minus_points - wjl_make_trouble_minus_points + wjl_supporter_points

    context = {
        'fxf_basic_points': fxf_basic_points,
        'wjl_basic_points': wjl_basic_points,
        'fxf_make_trouble_times': fxf_make_trouble_times,
        'wjl_make_trouble_times': wjl_make_trouble_times,
        'fxf_make_plus_10_times': fxf_make_plus_10_times,
        'wjl_make_plus_10_times': wjl_make_plus_10_times,
        'fxf_bonus_minus_points': fxf_bonus_minus_points,
        'wjl_bonus_minus_points': wjl_bonus_minus_points,
        'fxf_make_trouble_points': fxf_make_trouble_points,
        'wjl_make_trouble_points': wjl_make_trouble_points,
        'fxf_make_trouble_minus_points': fxf_make_trouble_minus_points,
        'wjl_make_trouble_minus_points': wjl_make_trouble_minus_points,
        'fxf_supporter_num': fxf_supporter_num,
        'wjl_supporter_num': wjl_supporter_num,
        'fxf_supporter_points': fxf_supporter_points,
        'wjl_supporter_points': wjl_supporter_points,
        'fxf_total_points': fxf_total_points,
        'wjl_total_points': wjl_total_points,
        'fxf_points': fxf_points,
        'wjl_points': wjl_points,
    }
    return render(request, 'modian/61-activity.html', context)


def birthday_index(request):
    logger.info('get all birthday wish, request: %s' % request)
    wishes = BirthdayWish.objects.order_by('-update_time')
    logger.info(wishes)

    provinceCode = {
        "11": "北京",
        "12": "天津",
        "31": "上海",
        "50": "重庆",
        "13": "河北",
        "41": "河南",
        "53": "云南",
        "21": "辽宁",
        "23": "黑龙江",
        "43": "湖南",
        "34": "安徽",
        "37": "山东",
        "65": "新疆",
        "32": "江苏",
        "33": "浙江",
        "36": "江西",
        "42": "湖北",
        "45": "广西",
        "62": "甘肃",
        "14": "山西",
        "15": "内蒙古",
        "61": "陕西",
        "22": "吉林",
        "35": "福建",
        "52": "贵州",
        "44": "广东",
        "63": "青海",
        "54": "西藏",
        "51": "四川",
        "64": "宁夏",
        "46": "海南",
        "101": "香港",
        "102": "澳门",
        "103": "台湾",
        "0": "海外"
    }

    for wish in wishes:
        logger.info(wish.province_code)
        wish.province = provinceCode[str(wish.province_code)]

    context = {
        'wishes': wishes
    }
    return render(request, 'birthdaywish/index.html', context)


def wish_form(request):
    return render(request, 'birthdaywish/form.html')


def submit_birthday_wish(request):
    import time
    logger.info(request)
    if request.method == 'POST':
        userid = request.POST['user_id']
        birthdaywish = request.POST['birthday_wish']
        province_code = request.POST['province_code']
        ip = request.POST['ip']
        time_str = utils.convert_timestamp_to_timestr(time.time() * 1000)
        wish = BirthdayWish(user_id=userid, province_code=province_code, birthday_wish=birthdaywish,
                            update_time=time_str, ip=ip)
        wish.save()
        return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        # form = BirthdayForm(request.POST)
        # logger.debug(form)
        #
        # if form.is_valid():
        #     userid = form.cleaned_data['user_id']
        #     birthdaywish = form.cleaned_data['birthday_wish']
        #     province_code = form.cleaned_data['province_code']
        #     ip = form.cleaned_data['ip']
        #     time_str = utils.convert_timestamp_to_timestr(time.time() * 1000)
        #
        #     wish = BirthdayWish(user_id=userid, province_code=province_code, birthday_wish=birthdaywish,
        #                         update_time=time_str, ip=ip)
        #     wish.save()
        #     return HttpResponse(json.dumps({'success': True}), content_type="application/json")
    return HttpResponse(json.dumps({'success': False}), content_type="application/json")


def get_all_birthday_wish(request):
    with connections['modian'].cursor() as cursor:
        cursor.execute("""
            select province_code, count(*) as num from `wish` group by province_code
        """)
        birthday_wish = utils.dictfetchall(cursor)
        logger.info(birthday_wish)
    return HttpResponse(json.dumps(birthday_wish), content_type='application/json')


def get_all_birthday_wish_2(request):
    logger.info('get all birthday wish, request: %s' % request)
    wishes = BirthdayWish.objects.order_by('-update_time')
    wishes_json = serializers.serialize("json", wishes)
    logger.info(wishes_json)
    return HttpResponse(json.dumps(wishes_json), content_type='application/json')
