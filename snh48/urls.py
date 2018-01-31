from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /member/10001
    url(r'^member/(?P<member_id>[0-9]+)', views.member_detail, name="member_detail"),
    url(r'^performance_history/(?P<performance_history_id>[0-9]+)', views.performance_history_detail, name="performance_history_detail"),
]