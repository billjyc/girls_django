# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import logging
import time

from django.core import serializers
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connections
from django.db.models import Q, Count, Window, F, Case, When, Value
from django.db.models.functions import ExtractYear, Coalesce
from django.db.models.functions.window import RowNumber
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.urls import reverse

from django_exercise import utils
from django_exercise.weibo_util import weibo_client
from .models import *

logger = logging.getLogger("django")


def get_teams_data():
    teams_data = cache.get('teams_data')
    if not teams_data:
        # 如果缓存中没有数据，则从数据库中读取
        teams_data = Team.objects.values('id', 'group', 'name')
        # 将数据存入缓存，设置过期时间为一天（86400秒）
        cache.set('teams_data', teams_data, 86400)
    return teams_data


# Create your views here.

def index(request):
    member_list = Memberinfo.objects.filter(
        is_valid=1
    ).order_by('id').order_by('team')
    # hiatus_list = Memberinfo.objects.filter(
    #     is_valid=0
    # ).order_by('id')
    context = {
        'team_sii': member_list.filter(team__id=101),
        'team_nii': member_list.filter(team__id=102),
        'team_hii': member_list.filter(team__id=103),
        'team_x': member_list.filter(team__id=104),
        # 'hiatus': hiatus_list
    }
    return render(request, 'snh48/index.html', context)


def hiatus_index(request):
    hiatus_list = Memberinfo.objects.filter(
        is_valid=0
    ).order_by('id')
    result = []
    for member in hiatus_list:
        if member.final_member_id == member.id:
            result.append(member)
    context = {
        'hiatus': result
    }
    return render(request, 'snh48/hiatus_index.html', context)


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
        ret = {'ability': serializers.serialize("json", ability),
               'info': serializers.serialize("json", [ability[0].member])}
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

    if request.GET.get('startDate'):
        where['date__gte'] = datetime.datetime.strptime(
            request.GET.get('startDate'), '%Y-%m-%d')
    if request.GET.get('endDate'):
        where['date__lte'] = datetime.datetime.strptime(
            request.GET.get('endDate'), '%Y-%m-%d') + datetime.timedelta(hours=23, minutes=59, seconds=59)
    if request.GET.get('team'):
        team = int(request.GET.get('team'))
        if team == 0:
            where['performance__team__exact'] = None
        elif team != -1:
            where['performance__team__exact'] = request.GET.get('team')

    if request.GET.get('performance'):
        where['performance__id__in'] = request.GET.getlist('performance')

    sort_name = request.GET.get('sort')
    if sort_name == 'date':
        sort_name = 'date'
    elif sort_name == 'team':
        sort_name = 'performance__team__name'
    elif sort_name == 'performance':
        sort_name = 'performance__name'
    else:
        sort_name = 'date'

    if request.GET.get('sortOrder') == 'asc':
        sort_order = ''
    else:
        sort_order = '-'

    # if request.GET.get('year'):
    #     where['date__year__in'] = request.GET.getlist('year')
    # if request.GET.get('team'):
    #     where['performance__team__in'] = request.GET.getlist('team')
    # if request.GET.get('performance'):
    #     where['performance__id__in'] = request.GET.getlist('performance')
    ph_list = PerformanceHistory.objects.filter(**where).order_by('{}{}'.format(sort_order, sort_name))

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

    if request.GET.get('startDate'):
        where['performance_history__date__gte'] = datetime.datetime.strptime(
            request.GET.get('startDate'), '%Y-%m-%d')
    if request.GET.get('endDate'):
        where['performance_history__date__lte'] = datetime.datetime.strptime(
            request.GET.get('endDate'), '%Y-%m-%d') + datetime.timedelta(hours=23, minutes=59, seconds=59)
    if request.GET.get('team'):
        team = int(request.GET.get('team'))
        if team == 0:
            where['performance_history__performance__team__exact'] = None
        elif team != -1:
            where['performance_history__performance__team__exact'] = request.GET.get('team')

    if request.GET.get('performance'):
        where['performance_history__performance__id__in'] = request.GET.getlist('performance')

    sort_name = request.GET.get('sort')
    if sort_name in ['view', 'danmaku']:
        pass
    elif sort_name == 'date':
        sort_name = 'performance_history__date'
    elif sort_name == 'team':
        sort_name = 'performance_history__performance__team__name'
    else:
        sort_name = 'view'

    if request.GET.get('sortOrder') == 'asc':
        sort_order = ''
    else:
        sort_order = '-'

    bilibili_list = BiliBiliStat.objects.filter(**where).exclude(
        aid__in=[25573155, 2512486, 2676912, 2517405]
    ).order_by('{}{}'.format(sort_order, sort_name))
    logger.info(bilibili_list.query)
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
    logger.info('获取成员详细信息: member_id: {}'.format(member_id))
    time0 = time.time()
    member = get_object_or_404(Memberinfo, pk=member_id)
    if member.final_member_id != int(member_id):
        redirect_url = f"/snh48/member/{member.final_member_id}"
        return redirect(redirect_url)

    transfer = Transfer.objects.filter(member_id=member_id).first()
    teams = get_teams_data()

    team_dict = {}
    for team_info in teams:
        team_dict[str(team_info['id'])] = f'{team_info["group"] if team_info["group"] else ""} {team_info["name"]}'

    if transfer:
        for transfer_detail in transfer.detail:
            description = utils.process_transfer_detail(transfer_detail, team_dict)
            transfer_detail['description'] = description

    with connections['snh48'].cursor() as cursor:
        cursor.execute("""
SELECT p.name as `performance_name`, ph.date as `date`, t.name as `team`, ph.description as `description`
FROM member_performance_history mph
JOIN performance_history ph ON mph.performance_history_id = ph.id
JOIN performance p ON p.id = ph.performance_id
LEFT JOIN team t ON t.id = p.team 
WHERE mph.member_id = %s
ORDER BY ph.date desc
        """, [member_id])
        member_performance_history_list = utils.namedtuplefetchall(cursor)
    ret_list = []
    for mph in member_performance_history_list:
        ret_list.append({
            "date": mph.date.strftime("%Y年%m月%d日 %H:%M"),
            "team": mph.team if mph.team else '',
            "performance": mph.performance_name,
            "description": mph.description
        })
    logger.debug(ret_list)

    ability = MemberAbility.objects.filter(member__id=member_id)
    logger.info('查询成员公演历史/能力耗时: {}s'.format(time.time() - time0))

    # 获取按照年份统计的公演场次数量
    performance_num_by_year_list = MemberPerformanceHistory.objects.filter(member_id=member_id).annotate(
        year=ExtractYear('performance_history__date')
    ).values('year').annotate(
        count=Count('id')
    ).order_by('-year')

    # 获取按照队伍统计的公演场次数量
    performance_num_by_team_list = MemberPerformanceHistory.objects.filter(
        member_id=member_id).values(team_id=Coalesce('performance_history__performance__team__id', 0),
                                    team_name=Case(
                                        When(performance_history__performance__team__name__isnull=False,
                                             then=F('performance_history__performance__team__name')),
                                        default=Value('联合公演'),
                                        output_field=models.CharField()
                                    )).annotate(
        count=Count('id')
    ).order_by('-count')

    # 获取unit表演阵容
    time0 = time.time()

    with connections['snh48'].cursor() as cursor:
        cursor.execute("""
SELECT uh.performance_history_id, DATE(ph.date) AS p_date, p.name, ph.description, u.id as unit_id, u.name AS unit_name, uh.rank AS unit_rank
FROM unit_history uh
JOIN unit u ON uh.`unit_id` = u.id
JOIN performance_history ph ON ph.id = uh.performance_history_id
JOIN performance p ON p.id = ph.performance_id
WHERE uh.member_id = %s
ORDER BY `p_date` desc, u.id, uh.rank;
            """, [member_id])
        unit_list = utils.namedtuplefetchall(cursor)
    logger.info('查询unit历史耗时: {}s'.format(time.time() - time0))

    # 获取微博粉丝数
    # 只取每天最新的数据
    time0 = time.time()
    weibo_fans_counts = WeiboDataHistory.objects.filter(member_id=member_id).order_by('update_time')
    logger.info('查询微博历史耗时: {}s'.format(time.time() - time0))
    fans_data = [{'date': count.update_time.strftime('%Y-%m-%d'),
                  'count': count.followers_count}
                 for count in weibo_fans_counts]

    context = {
        'member': member,
        'performance_num_by_year_list': performance_num_by_year_list,
        'performance_num_by_team_list': performance_num_by_team_list,
        'mph_list': ret_list,
        'total_performance_num': len(ret_list),
        'unit_list': unit_list,
        'weibo_fans_data': fans_data,
        "transfer_details": transfer.detail if transfer else []
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


def performance_num_rank_index(request):
    return render(request, 'snh48/performance_rank.html')


def performance_num_rank(request):
    limit = int(request.GET.get('limit', 1))
    offset = int(request.GET.get('offset', 50))
    team_id = request.GET.get('team', None)
    year = request.GET.get('year', None)
    is_valid = request.GET.get('is_valid', None)

    members = Memberinfo.objects.all()
    if is_valid:
        is_valid = int(is_valid)
        # members = members.filter(is_valid=is_valid)
        if is_valid == 1:
            members = members.filter(is_valid=is_valid, team__id__lt=199)
        elif is_valid == 0:
            members = members.filter(Q(is_valid=is_valid) |
                                     Q(team__id=199))
    if team_id:
        members = members.filter(team__id=team_id)
    if year:
        members = members.filter(memberperformancehistory__performance_history__date__year=year)

    # 筛选逻辑
    members = members.filter(Q(id__lt=20000)).annotate(
        num_performances=Count('memberperformancehistory')).annotate(
        rank=Window(
            expression=RowNumber(),
            order_by=F('num_performances').desc(),
        )
    ).order_by('-num_performances').order_by('rank')
    total = members.count()
    paginator = Paginator(members, limit)
    try:
        # 使用offset和limit计算当前是第几页
        page = offset // limit + 1
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)

    context = {
        "total": total,
        'rows': [
            {"rank": member.rank, "name": member.name, "team": member.team.name,
             "num_performances": member.num_performances, "id": member.id,
             "detail_url": reverse('snh48:member_detail', args=[member.id])}
            for member in members]
    }
    return JsonResponse(context)


def get_all_teams(request):
    teams = Team.objects.filter(id__lt=200, is_valid=1)
    return JsonResponse({'teams': list(teams.values('id', 'name'))})


def weibo_auth_request(request):
    """
    微博鉴权触发，会跳转到微博授权页面
    """
    authorize_url = weibo_client.get_authorize_url()
    logger.info('get weibo authorize url: %s' % authorize_url)
    return redirect(authorize_url)


def get_weibo_api_code(request):
    """
    在微博授权页面填写信息后，会跳转到这个页面，在url的get参数中获取code
    """
    code = request.GET.get('code', '')
    if not code:
        return HttpResponse(status=508, content={'msg': 'code is empty, please retry!'})
    logger.info('get weibo code: %s' % code)

    result = weibo_client.request_access_token(code)
    weibo_client.set_access_token(result.access_token, result.expires_in)

    logger.info('get access token: %s, expire in: %s' % (result.access_token, result.expires_in))
    return HttpResponse(status=200, content={'msg': 'Get weibo code success!', 'code': 0})
