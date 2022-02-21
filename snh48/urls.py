# -*- coding: utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('team/list/', views.team_list, name='team_list'),
    path('team/<int:team_id>', views.team_info, name='team_info'),

    path('index', views.index, name='index'),
    path('performance_history/index', views.performance_history_index, name='performance_history_index'),
    path('performance_history/list', views.get_performance_history_list, name='get_performance_history_list'),
    # ex: /member/10001
    path('member/<int:member_id>', views.member_detail, name="member_detail"),
    # ex: /performance_history/339
    path('performance_history/<int:performance_history_id>', views.performance_history_detail,
         name="performance_history_detail"),
    path('bilibili_stat/index', views.bilibili_stat_index, name='bilibili_stat_index'),
    path('bilibili_stat/get_bilibili_stat', views.get_bilibili_stat, name='get_bilibili_stat'),
    path('member/ability/<int:member_id>', views.member_ability, name='member_ability'),
    path('compare', views.compare, name='compare'),
    path('get_members_by_team/<int:team_id>', views.get_member_by_team, name='get_member_by_team')
]
