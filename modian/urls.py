from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='modian_index'),
    path('orders/<int:pro_id>/', views.get_all_orders, name='get_all_orders'),
    path('draw-records/', views.get_all_card_draw_record, name='get_all_draw_records'),
]
