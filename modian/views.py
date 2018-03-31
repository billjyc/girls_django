# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render

from .logic.modian_handler import ModianHandler
from .logic.card_draw_handler import CardDrawHandler
from .models import *


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the logic index.")


def get_all_orders(request, pro_id):
    modian_handler = ModianHandler()
    order_list = modian_handler.get_all_orders(pro_id)
    context = {
        'order_list': order_list,
    }
    return render(request, 'modian/orders.html', context)


def get_all_card_draw_record(request):
    records = DrawRecord.objects.order_by('-draw_time')
    context = {
        'records': records,
    }
    return render(request, 'modian/draw-records.html', context)


def get_card_draw_record(request):
    pass
