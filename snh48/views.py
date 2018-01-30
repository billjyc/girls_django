# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .models import *


# Create your views here.

def index(request):
    member_list = Memberinfo.objects.order_by('id')
    output = ', '.join([member.name for member in member_list])
    return HttpResponse(output)


def member_detail(request, member_id):
    return HttpResponse("You are looking at member %s" % member_id)