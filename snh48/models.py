# -*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class MemberPerformanceHistory(models.Model):
    member = models.ForeignKey('Memberinfo', models.DO_NOTHING, blank=True, null=True)
    performance_history = models.ForeignKey('PerformanceHistory', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member_performance_history'
        unique_together = (('member', 'performance_history'),)
        app_label = 'snh48'
        verbose_name = '成员公演记录'
        verbose_name_plural = '成员公演记录'


class MemberPerformanceHistoryTmp(models.Model):
    member = models.ForeignKey('Memberinfo', models.DO_NOTHING, blank=True, null=True)
    performance_history = models.ForeignKey('PerformanceHistory', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member_performance_history_tmp'
        unique_together = (('member', 'performance_history'),)
        app_label = 'snh48'
        verbose_name = '成员公演记录-本年度'
        verbose_name_plural = '成员公演记录-本年度'


class Memberinfo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name='姓名')
    nick_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='昵称')
    height = models.IntegerField(blank=True, null=True, verbose_name='身高')
    blood_type = models.CharField(max_length=10, blank=True, null=True, verbose_name='血型')
    team = models.ForeignKey('Team', models.DO_NOTHING, db_column='team', blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True, verbose_name='期数')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    english_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='英文名')
    join_time = models.DateField(blank=True, null=True, verbose_name='入团时间')
    link = models.CharField(max_length=300, blank=True, null=True, verbose_name='资料链接')
    image_link = models.CharField(max_length=300, blank=True, null=True, verbose_name='图片链接')
    hobby = models.CharField(max_length=100, blank=True, null=True, verbose_name='爱好')
    description = models.TextField(blank=True, null=True, verbose_name='备注')
    is_valid = models.IntegerField(verbose_name='是否在团')
    constellation = models.CharField(max_length=50, verbose_name='星座')
    birth_place = models.CharField(max_length=50, verbose_name='出生地')
    agency = models.CharField(max_length=50, verbose_name='日期')
    speciality = models.CharField(max_length=50, verbose_name='特长')
    pid = models.IntegerField(blank=True, null=True, verbose_name='期数编号')

    class Meta:
        managed = False
        db_table = 'memberinfo'
        app_label = 'snh48'
        verbose_name = '成员信息'
        verbose_name_plural = '成员信息'

    def __unicode__(self):
        return str(self.team) + '-' + self.name

    def __str__(self):
        return str(self.team) + '-' + self.name


class MemberAbility(models.Model):
    member = models.ForeignKey(Memberinfo, models.DO_NOTHING, db_column='member_id', blank=True, null=True)
    sing = models.IntegerField(db_column='sing', verbose_name='唱歌')
    dance = models.IntegerField(db_column='dance', verbose_name='舞蹈')
    variety = models.IntegerField(db_column='variety', verbose_name='综艺感')
    act = models.IntegerField(db_column='act', verbose_name='演技')
    health = models.IntegerField(db_column='health', verbose_name='健康')
    concentration = models.IntegerField(db_column='concentration', verbose_name='工作投入')
    leadership = models.IntegerField(db_column='leadership', verbose_name='领导力')
    ambition = models.IntegerField(db_column='ambition', verbose_name='野心')
    pressure = models.IntegerField(db_column='pressure', verbose_name='抗压能力')

    class Meta:
        managed = False
        db_table = 'ability'
        app_label = 'snh48'
        verbose_name = '成员能力'
        verbose_name_plural = '成员能力'

    def __unicode__(self):
        return str(self.member.name)

    def __str__(self):
        return str(self.member.name)


class Performance(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='公演名称')
    team = models.ForeignKey('Team', models.DO_NOTHING, db_column='team', blank=True, null=True)
    debut_date = models.DateField(blank=True, null=True, verbose_name='首演日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='千秋乐日期')
    link = models.CharField(max_length=200, blank=True, null=True, verbose_name='公演详情页链接')
    logo_link = models.CharField(max_length=100, verbose_name='公演logo链接')
    is_active = models.IntegerField(verbose_name='是否演出中')

    class Meta:
        managed = False
        db_table = 'performance'
        app_label = 'snh48'
        verbose_name = '公演信息'
        verbose_name_plural = '公演信息'

    def __unicode__(self):
        if self.team is None:
            return self.name
        return self.name + '-' +  str(self.team)

    def __str__(self):
        if self.team is None:
            return self.name
        return self.name + '-' +  str(self.team)


class Unit(models.Model):
    performance = models.ForeignKey('Performance', models.DO_NOTHING, db_column='performance_id', blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='歌曲名称')
    num = models.IntegerField(verbose_name='歌曲人数')

    class Meta:
        managed = False
        db_table = 'unit'
        app_label = 'snh48'
        verbose_name = 'Unit曲'
        verbose_name_plural = 'Unit曲'

    def __unicode__(self):
        return str(self.performance.name) + ' ' + self.name + ' 人数：' + str(self.num) + '人'

    def __str__(self):
        return str(self.performance.name) + ' ' + self.name + ' 人数：' + str(self.num) + '人'


class UnitHistory(models.Model):
    unit = models.ForeignKey('Unit', models.DO_NOTHING, db_column='unit_id', blank=True, null=True)
    performance_history = models.ForeignKey('PerformanceHistory', models.DO_NOTHING,
                                            db_column='performance_history_id', blank=True, null=True)
    member = models.ForeignKey('MemberInfo', models.DO_NOTHING, db_column='member_id', blank=True, null=True)
    rank = models.IntegerField(verbose_name='站位序号')

    class Meta:
        managed = False
        db_table = 'unit_history'
        app_label = 'snh48'
        verbose_name = 'Unit曲表演记录'
        verbose_name_plural = 'Unit曲表演记录'

    def __unicode__(self):
        return str(self.unit) + ' ' + str(self.member) + ' 顺位: ' + str(self.rank)

    def __str__(self):
        return str(self.unit) + ' ' + str(self.member) + ' 顺位: ' + str(self.rank)


class PerformanceHistory(models.Model):
    # performance_id = models.IntegerField(blank=True, null=True)
    performance = models.ForeignKey('Performance', models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True, verbose_name='公演时间')
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name='备注')
    video_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='视频链接')

    class Meta:
        managed = False
        db_table = 'performance_history'
        app_label = 'snh48'
        verbose_name = '公演日程'
        verbose_name_plural = '公演日程'

    def __unicode__(self):
        return str(self.date) + ' ' + str(self.performance) + ' ' + self.description

    def __str__(self):
        return str(self.date) + ' ' + str(self.performance) + ' ' + self.description


class BiliBiliStat(models.Model):
    performance_history = models.ForeignKey('PerformanceHistory', models.DO_NOTHING, db_column='performance_history_id')
    aid = models.IntegerField(verbose_name='视频BID')
    view = models.IntegerField(verbose_name='观看量')
    danmaku = models.IntegerField(verbose_name='弹幕数量')
    reply = models.IntegerField(verbose_name='评论数量')
    favorite = models.IntegerField(verbose_name='收藏数量')
    coin = models.IntegerField(verbose_name='投币数量')
    share = models.IntegerField(verbose_name='分享数量')
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bilibili_stat'
        app_label = 'snh48'
        verbose_name = '公演B站数据'
        verbose_name_plural = '公演B站数据'

    def __str__(self):
        return str(self.performance_history)


class Team(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='队伍编号')
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name='队伍名称')
    found_date = models.DateField(blank=True, null=True, verbose_name='建队时间')
    is_valid = models.IntegerField(blank=False, null=False, default=1)
    icon = models.CharField(max_length=500, blank=True, null=True)
    background_color = models.CharField(max_length=100, blank=True, null=True, verbose_name='应援色')

    class Meta:
        managed = False
        db_table = 'team'
        app_label = 'snh48'
        verbose_name = '队伍信息'
        verbose_name_plural = '队伍信息'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Weibo(models.Model):
    id = models.IntegerField(primary_key=True)
    weibo_id = models.BigIntegerField(blank=True, null=True)
    followers_count = models.BigIntegerField(blank=True, null=True)
    friends_count = models.BigIntegerField(blank=True, null=True)
    statuses_count = models.BigIntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weibo'
        app_label = 'snh48'
        verbose_name = '微博数据'
        verbose_name_plural = '微博数据'


class WeiboDataHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    weibo_id = models.BigIntegerField(blank=True, null=True)
    followers_count = models.BigIntegerField(blank=True, null=True)
    friends_count = models.BigIntegerField(blank=True, null=True)
    statuses_count = models.BigIntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weibo_data_history'
        app_label = 'snh48'
        verbose_name = '微博历史数据'
        verbose_name_plural = '微博历史数据'
