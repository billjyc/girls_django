# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import *


# Create your views here.

def index(request):
    member_list = Memberinfo.objects.filter(
        is_valid=1
    ).order_by('id').order_by('team')
    # template = loader.get_template('snh48/index.html')
    context = {
        'member_list': member_list,
    }
    return render(request, 'snh48/index.html', context)
    # return HttpResponse(template.render(context, request))


def member_detail(request, member_id):
    member = get_object_or_404(Memberinfo, pk=member_id)
    member_performance_history_list = MemberPerformanceHistory.objects.filter(member=member)
    context = {
        'member': member,
        'mph_list': member_performance_history_list
    }
    return render(request, 'snh48/member_detail.html', context)
