# -*- coding: utf-8 -*-
from django.urls import path

from . import drf_views
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('team/list/', views.team_list, name='team_list'),
    path('team/<int:team_id>', views.team_info, name='team_info'),
    path('team/get_all_teams/', views.get_all_teams, name='get_all_teams'),

    path('member/index', views.index, name='index'),
    path('member/hiatus_list', views.hiatus_index, name='hiatus_list'),
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
    path('get_members_by_team/<int:team_id>', views.get_member_by_team, name='get_member_by_team'),
    path('performance_rank/', views.performance_num_rank_index, name='performance_rank'),
    path('performance_rank/data/', views.performance_num_rank, name='performance_rank_data'),

    # weibo authorize
    path('weibo/auth/request', views.weibo_auth_request, name='weibo_auth_request'),
    path('weibo/get_code/', views.get_weibo_api_code, name='get_weibo_api_code'),

    # Django restful framework 接口
    path('api/get_members_by_team_id/<int:team_id>', drf_views.get_member_by_team_id, name='drf_get_member_by_team_id'),
    path('api/performance/get_performance_list', drf_views.get_performance_list, name='drf_get_performance_list'),
    path('api/member/<int:member_id>', drf_views.get_member_profile, name="drf_member_detail"),
    path('api/performance/<int:performance_id>', drf_views.get_stage_detail, name="drf_stage_detail"),
    path('api/get_performance_history', drf_views.get_performance_history_list, name="drf_performance_history"),
    path('api/senbatsu_election/list', drf_views.get_senbatsu_election_list, name="drf_senbatsu_election_list"),
    path('api/senbatsu_election/<int:election_order>', drf_views.get_senbatsu_election_detail, name="drf_senbatsu_election_detail"),

]
