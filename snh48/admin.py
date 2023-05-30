# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Register your models here.
# admin.site.register(Team)
# admin.site.register(Memberinfo)
# admin.site.register(Performance)
# admin.site.register(PerformanceHistory)
admin.site.register(MemberPerformanceHistory)
admin.site.register(MemberPerformanceHistoryTmp)


# admin.site.register(Unit)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'found_date', 'get_is_valid_display')
    list_filter = ('is_valid',)  # 在侧边栏添加过滤器
    search_fields = ('name',)  # 在顶部添加搜索字段
    list_per_page = 50
    date_hierarchy = 'found_date'

    def get_is_valid_display(self, obj):
        return '是' if obj.is_valid == 1 else '否'

    get_is_valid_display.short_description = '是否活跃中'


@admin.register(Memberinfo)
class MemberInfoAdmin(admin.ModelAdmin):
    empty_value_display = "N/A"
    ordering = ['id']
    list_display = ('id', "avatar", 'name', 'team', 'pid', 'batch', 'birthday', 'join_time', 'get_is_valid_display')  # 自定义显示的字段
    list_filter = ('team', 'is_valid', 'batch')  # 在侧边栏添加过滤器
    search_fields = ('name',)  # 在顶部添加搜索字段
    list_per_page = 50
    date_hierarchy = 'birthday'
    list_editable = ('team', 'birthday')

    @admin.display(empty_value="暂无图片")
    def avatar(self, obj):
        return format_html("<img src='{}' width='50%'></img>".format(obj.image_link))

    @admin.display(description="是否在团")
    def get_is_valid_display(self, obj):
        return '是' if obj.is_valid == 1 else '否'


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'team', 'debut_date', 'end_date', 'get_is_active_display')
    list_filter = ('team', 'is_active',)  # 在侧边栏添加过滤器
    search_fields = ('name',)  # 在顶部添加搜索字段
    list_per_page = 50
    date_hierarchy = 'debut_date'

    def get_is_active_display(self, obj):
        return '是' if obj.is_active == 1 else '否'

    get_is_active_display.short_description = '是否演出中'


class MemberPerformanceHistoryInline(admin.TabularInline):
    model = MemberPerformanceHistory
    extra = 16


class MemberPerformanceHistoryTmpInline(admin.TabularInline):
    model = MemberPerformanceHistoryTmp
    extra = 16


@admin.register(PerformanceHistory)
class PerformanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'performance', 'date', 'description', 'video_url')
    list_filter = ('performance', 'performance__team',)  # 在侧边栏添加过滤器
    search_fields = ('description', 'performance__name')  # 在顶部添加搜索字段
    list_per_page = 50
    date_hierarchy = 'date'
    list_display_links = ['performance']
    inlines = [MemberPerformanceHistoryInline, MemberPerformanceHistoryTmpInline]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'performance', 'name', 'num')
    list_per_page = 50
    search_fields = ['performance__name', 'name']  # 搜索字段
    list_display_links = ['performance']
    # date_hierarchy = 'performance_history__date'
    list_filter = ('performance', 'num')  # 过滤器


@admin.register(UnitHistory)
class UnitHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'member', 'performance_history')

    list_per_page = 50

    search_fields = ['unit__name', 'member__name']  # 搜索字段

    list_display_links = ['unit']

    date_hierarchy = 'performance_history__date'

    list_filter = ('member', 'unit')  # 过滤器
