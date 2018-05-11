# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render

from .logic.modian_handler import ModianHandler
from .logic.card_draw_handler import CardDrawHandler
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
import logging

logger = logging.getLogger('django')


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the logic index.")


def get_all_orders(request, pro_id):
    # modian_handler = ModianHandler()
    page = request.GET.get('page', 1)
    logger.debug('page: %s', page)
    order_list = Order.objects.filter(pro_id=pro_id)
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
