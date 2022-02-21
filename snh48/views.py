# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, HttpResponse
from django.db import connection, connections
from django.db.models import Q
import datetime
import json
from django.core import serializers

from .models import *
from django_exercise import utils
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    member_list = Memberinfo.objects.filter(
        is_valid=1
    ).order_by('id').order_by('team')
    hiatus_list = Memberinfo.objects.filter(
        is_valid=0
    ).order_by('id')
    context = {
        'team_sii': member_list.filter(team__id=101),
        'team_nii': member_list.filter(team__id=102),
        'team_hii': member_list.filter(team__id=103),
        'team_x': member_list.filter(team__id=104),
        'hiatus': hiatus_list
    }
    return render(request, 'snh48/index.html', context)


def compare(request):
    team_list = Team.objects.filter(is_valid=1)
    member_list = Memberinfo.objects.filter(is_valid=1)

    member_dict = {}
    for member in member_list:
        if str(member.team.id) not in member_dict:
            member_dict[str(member.team.id)] = []
        member_dict[str(member.team.id)].append(member)

    context = {
        'team_list': team_list,
        'member_list': member_dict
    }
    return render(request, 'snh48/compare.html', context)


def get_member_by_team(request, team_id):
    member_list = Memberinfo.objects.filter(is_valid=1).filter(team__id=team_id)
    logger.debug(member_list)
    member_list_json = serializers.serialize("json", member_list)
    return HttpResponse(member_list_json)


def team_list(request):
    context = {

    }
    return render(request, 'snh48/team_list.html', context)


def member_ability(request, member_id):
    ability = MemberAbility.objects.filter(member__id=member_id)
    if ability:
        ret = {'ability': serializers.serialize("json", ability), 'info': serializers.serialize("json", [ability[0].member])}
    else:
        ret = {}

    return HttpResponse(json.dumps(ret))


def team_info(request, team_id):
    member_list = Memberinfo.objects.filter(team__id=team_id).filter(
        is_valid=1
    ).order_by('id')
    team_detail = Team.objects.get(pk=team_id)
    context = {
        'member_list': member_list,
        'team_detail': team_detail
    }

    return render(request, 'snh48/team_info.html', context)


def get_performance_history_list(request):
    page = request.GET.get('page', 1)
    row = request.GET.get('rows', 100)
    where = {}
    if request.GET.get('year'):
        where['date__year__in'] = request.GET.getlist('year')
    if request.GET.get('team'):
        where['performance__team__in'] = request.GET.getlist('team')
    if request.GET.get('performance'):
        where['performance__id__in'] = request.GET.getlist('performance')
    ph_list = PerformanceHistory.objects.filter(**where).order_by('-date')

    if request.GET.get('keywords'):
        keywords = request.GET.get('keywords')
        ph_list = ph_list.filter(Q(description__icontains=keywords) |
                                       Q(performance__name__icontains=keywords) |
                                       Q(performance__team__name__icontains=keywords))
    paginator = Paginator(ph_list, row)
    logger.info(ph_list.query)
    total = len(ph_list)
    try:
        ph_list = paginator.page(page)
    except PageNotAnInteger:
        ph_list = paginator.page(1)
    except EmptyPage:
        ph_list = paginator.page(paginator.num_pages)

    ret_list = []
    for performance_history in ph_list:
        ret_list.append({
            "id": performance_history.id,
            "date": performance_history.date.strftime("%Y年%m月%d日 %H:%M"),
            "team": performance_history.performance.team.name if performance_history.performance.team else '',
            "performance": performance_history.performance.name,
            "description": performance_history.description
        })
    logger.debug(ret_list)
    ret = {
        "total": total,
        'rows': ret_list,
    }
    return HttpResponse(json.dumps(ret))


def performance_history_index(request):
    return render(request, 'snh48/performance_history_index.html')


def get_bilibili_stat(request):
    page = request.GET.get('page', 1)
    row = request.GET.get('rows', 100)
    # 筛选逻辑
    where = {}
    if request.GET.get('year'):
        where['performance_history__date__year__in'] = request.GET.getlist('year')
    if request.GET.get('team'):
        where['performance_history__performance__team__in'] = request.GET.getlist('team')
    if request.GET.get('performance'):
        where['performance_history__performance__id__in'] = request.GET.getlist('performance')

    bilibili_list = BiliBiliStat.objects.filter(**where).exclude(
        aid__in=[25573155, 2512486, 2676912, 2517405]
    ).order_by('-view')

    if request.GET.get('keywords'):
        keywords = request.GET.get('keywords')
        bilibili_list = bilibili_list.filter(Q(performance_history__description__icontains=keywords) |
                                             Q(performance_history__performance__name__icontains=keywords) |
                                             Q(performance_history__performance__team__name__icontains=keywords))
        # where['performance_history__description__icontains'] = request.GET.get('keywords')
    logger.info(bilibili_list.query)
    total = len(bilibili_list)
    paginator = Paginator(bilibili_list, row)

    try:
        bilibili_list = paginator.page(page)
    except PageNotAnInteger:
        bilibili_list = paginator.page(1)
    except EmptyPage:
        bilibili_list = paginator.page(paginator.num_pages)

    ret_list = []
    for bilibili_stat in bilibili_list:
        ret_list.append({
            "performance_history_id": bilibili_stat.performance_history.id,
            "date": bilibili_stat.performance_history.date.strftime("%Y年%m月%d日 %H:%M"),
            "aid": bilibili_stat.aid,
            "team": bilibili_stat.performance_history.performance.team.name if bilibili_stat.performance_history.performance.team else '',
            "performance": bilibili_stat.performance_history.performance.name,
            "remark": bilibili_stat.performance_history.description,
            "view": bilibili_stat.view,
            "danmaku": bilibili_stat.danmaku,
            "reply": bilibili_stat.reply,
            "favorite": bilibili_stat.favorite,
            "coin": bilibili_stat.coin,
            "share": bilibili_stat.share
        })
    logger.debug(ret_list)
    ret = {
        "rows": ret_list,
        "total": total
    }
    return HttpResponse(json.dumps(ret))


def bilibili_stat_index(request):
    return render(request, 'snh48/bilibili_stat_index.html')


def member_detail(request, member_id):
    """
    获取成员详情
    :param request:
    :param member_id: 成员id
    :return:
    """
    member = get_object_or_404(Memberinfo, pk=member_id)
    member_performance_history_list = MemberPerformanceHistory.objects.filter(member=member).order_by('-performance_history__date')
    ability = MemberAbility.objects.filter(member__id=member_id)

    # 获取unit表演阵容
    with connections['snh48'].cursor() as cursor:
        cursor.execute("""
                SELECT uh.performance_history_id, DATE(ph.date) AS p_date, p.name, ph.description, u.id as unit_id, u.name AS unit_name, uh.rank AS unit_rank
FROM unit u, unit_history uh, performance_history ph, performance p
WHERE uh.member_id = %s AND uh.`unit_id` = u.id AND ph.id = uh.performance_history_id AND p.id = ph.performance_id
ORDER BY `p_date` desc, u.id, uh.rank;

            """, [member_id])
        unit_list = utils.namedtuplefetchall(cursor)
    context = {
        'member': member,
        'mph_list': member_performance_history_list,
        'unit_list': unit_list
    }
    if ability:
        context['ability'] = ability[0]
    else:
        context['ability'] = None
    return render(request, 'snh48/member_detail.html', context)


def performance_history_detail(request, performance_history_id):
    ph = PerformanceHistory.objects.get(pk=performance_history_id)
    member_list = MemberPerformanceHistory.objects.filter(performance_history=ph)
    bs = BiliBiliStat.objects.filter(performance_history=ph)

    # 获取unit表演阵容
    with connections['snh48'].cursor() as cursor:
        cursor.execute("""
            SELECT mi.id, mi.name AS member_name, uh.performance_history_id, u.id AS unit_id, u.name AS unit_name, uh.rank AS unit_rank
FROM memberinfo mi, unit u, unit_history uh
WHERE uh.performance_history_id = %s AND mi.id = uh.`member_id` AND uh.`unit_id` = u.id
ORDER BY uh.`performance_history_id`, u.id, uh.rank;

        """, [performance_history_id])
        unit_list = utils.namedtuplefetchall(cursor)
    context = {
        'ph': ph,
        'member_list': member_list,
        'unit_list': unit_list,
        'bs': bs,
    }
    return render(request, 'snh48/performance_history_detail.html', context)
