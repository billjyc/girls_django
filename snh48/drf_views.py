# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db import connections, models
from django.db.models import Count, Case, When, Value, F
from django.db.models.functions import ExtractYear, Coalesce
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django_exercise import utils
from snh48.models import Performance, Team, PerformanceHistory, Memberinfo, Transfer, MemberAbility, \
    MemberPerformanceHistory, WeiboDataHistory
from snh48.serializers import PerformanceSerializer, MemberSerializer, TeamSerializer, MemberAbilitySerializer
import logging

from snh48.views import get_teams_data

logger = logging.getLogger("django")


@api_view(['GET'])
def get_member_profile(request, member_id):
    logger.info('获取成员详细信息: member_id: {}'.format(member_id))
    time0 = time.time()
    member = get_object_or_404(Memberinfo, pk=member_id)
    if member.final_member_id != int(member_id):
        redirect_url = f"/member/{member.final_member_id}"
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
    logger.debug('查询成员公演历史/能力耗时: {}s'.format(time.time() - time0))

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
    logger.debug('查询unit历史耗时: {}s'.format(time.time() - time0))

    # 获取微博粉丝数
    # 只取每天最新的数据
    time0 = time.time()
    weibo_fans_counts = WeiboDataHistory.objects.filter(member_id=member_id).order_by('update_time')
    logger.debug('查询微博历史耗时: {}s'.format(time.time() - time0))
    fans_data = [{'date': count.update_time.strftime('%Y-%m-%d'),
                  'count': count.followers_count}
                 for count in weibo_fans_counts]

    serializer = MemberSerializer(member, many=False)

    context = {
        'member': serializer.data,
        'performance_num_by_year_list': performance_num_by_year_list,
        'performance_num_by_team_list': performance_num_by_team_list,
        'mph_list': ret_list,
        'total_performance_num': len(ret_list),
        'unit_list': unit_list,
        'weibo_fans_data': fans_data,
        "transfer_details": transfer.detail if transfer else []
    }
    if ability:
        ability_serializer = MemberAbilitySerializer(ability[0], many=False)
        context['ability'] = ability_serializer.data
    else:
        context['ability'] = None

    response_data = {
        'code': 0,
        'msg': 'ok',
        'result': context,
    }
    return Response(response_data)


@api_view(['GET'])
def get_performance_list(request):
    """
    获取公演列表
    :param request:
    :return:
    """
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    performance_list = Performance.objects.filter(team_id__lt=200)
    serializer = PerformanceSerializer(performance_list, many=True)

    result = {'0': {
        'id': 0,
        'name': '其他',
        'headerColor': '',
        'detail': []
    }}
    raw_data = serializer.data
    for p in raw_data:
        if 'team' in p:
            team_detail = get_object_or_404(Team, pk=p['team'])
            if p['team'] not in result:
                result[p['team']] = {
                    'id': p['team'],
                    'name': team_detail.name,
                    'headerColor': team_detail.background_color,
                    'detail': []
                }
            p['nums'] = PerformanceHistory.objects.filter(performance__id=p['id']).count()
            result[p['team']]['detail'].append(p)
        else:
            result['0']['detail'].append(p)

    result2 = []
    # 只需要拿到value就可以
    for k, v in result.items():
        # 公演按照首演日期排序
        v['detail'].sort(key=lambda x: x['debut_date'])
        result2.append(v)

    response_data = {
        'code': 0,
        'msg': 'ok',
        'result': result2
    }
    return Response(response_data)


@api_view(['GET'])
def get_member_by_team_id(request, team_id):
    """
    根据队伍id获取列表
    :param request:
    :param team_id:
    :return:
    """
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    member_list = Memberinfo.objects.filter(is_valid=1).filter(team__id=team_id).order_by('id')
    logger.debug(member_list)
    # 将成员列表序列化为 JSON
    serializer = MemberSerializer(member_list, many=True)
    team_detail = get_object_or_404(Team, pk=team_id)
    team_serializer = TeamSerializer(team_detail)
    response_data = {
        'code': 0,
        'msg': 'ok',
        'result': {
            'member_list': serializer.data,
            'team': team_serializer.data
        },
    }
    # 返回 JSON 响应
    return Response(response_data)
