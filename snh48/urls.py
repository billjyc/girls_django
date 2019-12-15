from django.conf.urls import url
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('team/list/', views.team_list, name='team_list'),
    url(r'^team/(?P<team_id>[0-9]+)', views.team_info, name='team_info'),
    url(r'^$', views.team_list, name='team_list'),
    url(r'^index', views.index, name='index'),
    url(r'^performance_history/index', views.performance_history_index, name='performance_history_index'),
    # ex: /member/10001
    url(r'^member/(?P<member_id>[0-9]+)', views.member_detail, name="member_detail"),
    # ex: /performance_history/339
    url(r'^performance_history/(?P<performance_history_id>[0-9]+)', views.performance_history_detail, name="performance_history_detail"),
    # url(r'^orders/(?P<pro_id>[0-9]+)', views.get_all_orders, name='get_all_orders'),
    url(r'^bilibili_stat/index', views.bilibili_stat_index, name='bilibili_stat_index'),
]
