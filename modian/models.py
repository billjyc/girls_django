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


class SeatsRecord(models.Model):
    id = models.IntegerField(primary_key=True)
    supporter = models.ForeignKey('Supporter', models.DO_NOTHING, db_column='modian_id')
    seats_type = models.IntegerField(db_column='seats_type')
    seats_number = models.IntegerField(db_column='seats_number')
    update_time = models.DateTimeField(db_column='update_time')

    def __unicode__(self):
        return 'SeatsRecord[supporter_id=%s, supporter_name=%s, seats_type=%s, seats_number=%s]' \
                % (self.supporter.id, self.supporter.name, self.seats_type, self.seats_number)

    def __str__(self):
        return 'SeatsRecord[supporter_id=%s, supporter_name=%s, seats_type=%s, seats_number=%s]' \
               % (self.supporter.id, self.supporter.name, self.seats_type, self.seats_number)

    class Meta:
        managed = False
        db_table = 'seats_record'


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
    # card = models.ForeignKey('Card', models.DO_NOTHING, db_column='card_id')
    card_id = models.IntegerField(db_column='card_id')
    draw_time = models.DateTimeField()
    backer_money = models.FloatField(db_column='backer_money')

    class Meta:
        managed = False
        db_table = 'draw_record'


class DrawFuRecord(models.Model):
    supporter = models.ForeignKey('Supporter', models.DO_NOTHING, db_column='supporter_id')
    # card = models.ForeignKey('Card', models.DO_NOTHING, db_column='card_id')
    fu_idx = models.IntegerField(db_column='fu_idx')
    fu_name = models.CharField(db_column='fu_name', max_length=100)
    update_time = models.DateTimeField(db_column='update_time')
    # backer_money = models.FloatField(db_column='backer_money')

    class Meta:
        managed = False
        db_table = 't_draw_fu_record'


class BirthdayWish(models.Model):
    user_id = models.CharField(max_length=30, db_column='user_id')
    birthday_wish = models.CharField(max_length=100, db_column='wish')
    province_code = models.IntegerField(db_column='province_code')
    update_time = models.DateTimeField(db_column='update_time')
    ip = models.CharField(max_length=100, db_column='ip', primary_key=True)

    class Meta:
        managed = False
        db_table = 'wish'

    def __unicode__(self):
        return 'BirthdayWish[user_id=%s, birthday_wish=%s, ip=%s, province_code=%s, update_time=%s]' % (self.user_id, self.birthday_wish, self.ip, self.province_code, self.update_time)

    def __str__(self):
        return 'BirthdayWish[user_id=%s, birthday_wish=%s, ip=%s, province_code=%s, update_time=%s]' % (self.user_id, self.birthday_wish, self.ip, self.province_code, self.update_time)
