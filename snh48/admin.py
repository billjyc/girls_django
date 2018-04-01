# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Team)
admin.site.register(Memberinfo)
admin.site.register(Performance)
admin.site.register(PerformanceHistory)
admin.site.register(MemberPerformanceHistory)
admin.site.register(MemberPerformanceHistoryTmp)
admin.site.register(Unit)


@admin.register(UnitHistory)
class UnitHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'member', 'performance_history')

    list_per_page = 50

    search_fields = ['unit__name', 'member__name']  # 搜索字段

    list_display_links = ['unit']

    date_hierarchy = 'performance_history__date'

    list_filter = ('member', 'unit')  # 过滤器

