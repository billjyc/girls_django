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


class MemberPerformanceHistoryTmp(models.Model):
    member = models.ForeignKey('Memberinfo', models.DO_NOTHING, blank=True, null=True)
    performance_history = models.ForeignKey('PerformanceHistory', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member_performance_history_tmp'
        unique_together = (('member', 'performance_history'),)


class Memberinfo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    blood_type = models.CharField(max_length=10, blank=True, null=True)
    team = models.IntegerField(blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    english_name = models.CharField(max_length=50, blank=True, null=True)
    join_time = models.DateField(blank=True, null=True)
    link = models.CharField(max_length=300, blank=True, null=True)
    image_link = models.CharField(max_length=300, blank=True, null=True)
    hobby = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_valid = models.IntegerField()
    constellation = models.CharField(max_length=50)
    birth_place = models.CharField(max_length=50)
    agency = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)
    pid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'memberinfo'


class Performance(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    team = models.ForeignKey('Team', models.DO_NOTHING, db_column='team', blank=True, null=True)
    debut_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    logo_link = models.CharField(max_length=100)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'performance'


class PerformanceHistory(models.Model):
    performance_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'performance_history'


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    found_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'


class Weibo(models.Model):
    id = models.IntegerField(blank=True, null=True)
    weibo_id = models.BigIntegerField(blank=True, null=True)
    followers_count = models.BigIntegerField(blank=True, null=True)
    friends_count = models.BigIntegerField(blank=True, null=True)
    statuses_count = models.BigIntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weibo'


class WeiboDataHistory(models.Model):
    id = models.ForeignKey(Memberinfo, models.DO_NOTHING, db_column='id', blank=True, null=True)
    weibo_id = models.BigIntegerField(blank=True, null=True)
    followers_count = models.BigIntegerField(blank=True, null=True)
    friends_count = models.BigIntegerField(blank=True, null=True)
    statuses_count = models.BigIntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weibo_data_history'
