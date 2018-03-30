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


class Card(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'card'

    def __unicode__(self):
        return 'Card[name=%s, level=%s]' % (self.name, self.level)


class DrawRecord(models.Model):
    supporter_id = models.ForeignKey('Supporter', models.DO_NOTHING, db_column='supporter_id')
    card_id = models.ForeignKey('Card', models.DO_NOTHING, db_column='card_id')
    draw_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'draw_record'
