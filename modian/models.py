# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Supporter(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'supporter'

    def __unicode__(self):
        return 'Supporter[id=%s, name=%s]' % (self.id, self.name)

    def __str__(self):
        return 'Supporter[id=%s, name=%s]' % (self.id, self.name)


class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    supporter = models.ForeignKey('Supporter', models.DO_NOTHING, db_column='supporter_id')
    backer_money = models.FloatField(db_column='backer_money')
    pay_time = models.DateTimeField(db_column='pay_time')
    pro_id = models.IntegerField(db_column='pro_id')

    class Meta:
        managed = False
        db_table = 'order'

    def __unicode__(self):
        return 'Order[pro_id=%s, supporter=%s, pay_time=%s, backer_money=%s]' \
               % (self.pro_id, self.supporter.name, self.pay_time, self.backer_money)

    def __str__(self):
        return 'Order[pro_id=%s, supporter=%s, pay_time=%s, backer_money=%s]' \
               % (self.pro_id, self.supporter.name, self.pay_time, self.backer_money)


class Card(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'card'

    def __unicode__(self):
        return 'Card[name=%s, level=%s]' % (self.name, self.level)

    def __str__(self):
        return 'Card[name=%s, level=%s]' % (self.name, self.level)


class DrawRecord(models.Model):
    supporter = models.ForeignKey('Supporter', models.DO_NOTHING, db_column='supporter_id')
    card = models.ForeignKey('Card', models.DO_NOTHING, db_column='card_id')
    draw_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'draw_record'
