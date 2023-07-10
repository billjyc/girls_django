# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from snh48.models import Performance, Team, PerformanceHistory, Memberinfo
from snh48.serializers import PerformanceSerializer, MemberSerializer, TeamSerializer
import logging


logger = logging.getLogger("django")


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
        v['detail'].sort(key=lambda x:x['debut_date'])
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
