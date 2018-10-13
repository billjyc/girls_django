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


def submit_birthday_wish(request):
    if request.method == 'POST':
        form = BirthdayForm(request.POST)

        if form.is_valid():
            userid = form.cleaned_data['userid']
            birthdaywish = form.cleaned_data['birthdaywish']
            province_code = 10

            wish = BirthdayWish(user_id=userid, province_code=province_code, birthday_wish=birthdaywish)
            wish.save()
            return {'success': True}
    return {'success': False}
