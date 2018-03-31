# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render

from .logic.modian_handler import ModianHandler
from django_exercise import utils


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
