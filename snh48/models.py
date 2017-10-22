# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class MemberInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=100)
    height = models.IntegerField()
    blood_type = models.CharField(max_length=10)
    team = models.IntegerField()
    batch = models.CharField(max_length=100)
    batch_no = models.IntegerField()
    birthday = models.DateField()
    english_name = models.CharField(max_length=50)
    join_time = models.DateField()
    link = models.CharField(max_length=300)  # 官网链接
    image_link = models.CharField(max_length=300)  # 公式照链接
    hobby = models.CharField(max_length=200)  # 爱好
    description = models.TextField()  # 经历
    is_valid = models.IntegerField()  # 是否为暂休
    constellation = models.CharField(max_length=50)  # 星座
    birth_place = models.CharField(max_length=50)
    agency = models.CharField(max_length=50)
    speciality = models.CharField(max_length=500)  # 特长


