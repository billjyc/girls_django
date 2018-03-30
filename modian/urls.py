from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='modian_index'),
    url(r'^orders/(?P<pro_id>[0-9]+)', views.get_all_orders, name='get_all_orders'),
]