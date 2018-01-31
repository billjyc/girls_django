# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from .models import *


# Create your views here.

def index(request):
    member_list = Memberinfo.objects.filter(
        is_valid=1
    ).order_by('id').order_by('team')
    context = {
        'team_sii': member_list.filter(team__id=1),
        'team_nii': member_list.filter(team__id=2),
        'team_hii': member_list.filter(team__id=3),
        'team_x': member_list.filter(team__id=4),
        'team_xii': member_list.filter(team__id=5),
    }
    return render(request, 'snh48/index.html', context)


def performance_history_index(request):
    ph_list = PerformanceHistory.objects.order_by('-id')
    context = {
        'ph_list': ph_list,
    }
    return render(request, 'snh48/performance_history_index.html', context)


def member_detail(request, member_id):
    """
    获取成员详情
    :param request:
    :param member_id: 成员id
    :return:
    """
    member = get_object_or_404(Memberinfo, pk=member_id)
    member_performance_history_list = MemberPerformanceHistory.objects.filter(member=member).order_by('-performance_history_id')
    context = {
        'member': member,
        'mph_list': member_performance_history_list,
    }
    return render(request, 'snh48/member_detail.html', context)


def performance_history_detail(request, performance_history_id):
    ph = PerformanceHistory.objects.get(pk=performance_history_id)
    member_list = MemberPerformanceHistory.objects.filter(performance_history=ph)
    context = {
        'ph': ph,
        'member_list': member_list,
    }
    return render(request, 'snh48/performance_history_detail.html', context)
