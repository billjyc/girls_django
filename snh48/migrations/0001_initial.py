# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-29 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Memberinfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('nick_name', models.CharField(blank=True, max_length=100, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('blood_type', models.CharField(blank=True, max_length=10, null=True)),
                ('batch', models.CharField(blank=True, max_length=100, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('english_name', models.CharField(blank=True, max_length=50, null=True)),
                ('join_time', models.DateField(blank=True, null=True)),
                ('link', models.CharField(blank=True, max_length=300, null=True)),
                ('image_link', models.CharField(blank=True, max_length=300, null=True)),
                ('hobby', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_valid', models.IntegerField()),
                ('constellation', models.CharField(max_length=50)),
                ('birth_place', models.CharField(max_length=50)),
                ('agency', models.CharField(max_length=50)),
                ('speciality', models.CharField(max_length=50)),
                ('pid', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'memberinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MemberPerformanceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'member_performance_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MemberPerformanceHistoryTmp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'member_performance_history_tmp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('debut_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
                ('logo_link', models.CharField(max_length=100)),
                ('is_active', models.IntegerField()),
            ],
            options={
                'db_table': 'performance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PerformanceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('video_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'performance_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('found_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'team',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('num', models.IntegerField()),
            ],
            options={
                'db_table': 'unit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UnitHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
            ],
            options={
                'db_table': 'performance_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Weibo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('weibo_id', models.BigIntegerField(blank=True, null=True)),
                ('followers_count', models.BigIntegerField(blank=True, null=True)),
                ('friends_count', models.BigIntegerField(blank=True, null=True)),
                ('statuses_count', models.BigIntegerField(blank=True, null=True)),
                ('update_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'weibo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WeiboDataHistory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('weibo_id', models.BigIntegerField(blank=True, null=True)),
                ('followers_count', models.BigIntegerField(blank=True, null=True)),
                ('friends_count', models.BigIntegerField(blank=True, null=True)),
                ('statuses_count', models.BigIntegerField(blank=True, null=True)),
                ('update_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'weibo_data_history',
                'managed': False,
            },
        ),
    ]
