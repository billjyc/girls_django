from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='modian_index'),
    path('orders/<int:pro_id>/', views.get_all_orders, name='get_all_orders'),
    path('draw-records/', views.get_all_card_draw_record, name='get_all_draw_records'),
    path('score/', views.get_score_detail, name='get_score_detail'),
    path('draw-records-statistics/', views.get_card_draw_record_by_supporter, name='get_draw_record_by_supporter'),
    path('draw-fu-records/', views.get_draw_fu_record, name='get_all_draw_fu_records'),
    path('draw-fu-records-statistics/', views.get_fu_draw_record_by_supporter, name='get_draw_fu_record_by_supporter'),
    # path('61-activity/', views.get_61_pk_detail, name='get_61_pk_detail'),
    # path('300-activity/', views.get_300_activity_detail, name='get_300_detail'),
    # 2018生日特别活动
    path('birthday-index', views.birthday_index, name="birthday_index"),
    # path('wish-form', views.wish_form, name="wish_form"),
    # path('submit-birthday-wish/', views.submit_birthday_wish, name='submit_birthday_wish'),
    path('get-birthday-wish/', views.get_all_birthday_wish, name='get_birthday_wish'),
    # path('get-birthday-wish-2/', views.get_all_birthday_wish_2, name='get_birthday_wish2')
]
