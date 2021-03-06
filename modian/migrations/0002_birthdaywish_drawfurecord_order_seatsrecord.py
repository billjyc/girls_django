# Generated by Django 3.1.1 on 2020-09-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modian', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BirthdayWish',
            fields=[
                ('user_id', models.CharField(db_column='user_id', max_length=30)),
                ('birthday_wish', models.CharField(db_column='wish', max_length=100)),
                ('province_code', models.IntegerField(db_column='province_code')),
                ('update_time', models.DateTimeField(db_column='update_time')),
                ('ip', models.CharField(db_column='ip', max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'wish',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DrawFuRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fu_idx', models.IntegerField(db_column='fu_idx')),
                ('fu_name', models.CharField(db_column='fu_name', max_length=100)),
                ('update_time', models.DateTimeField(db_column='update_time')),
            ],
            options={
                'db_table': 't_draw_fu_record',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('backer_money', models.FloatField(db_column='backer_money')),
                ('pay_time', models.DateTimeField(db_column='pay_time')),
                ('pro_id', models.IntegerField(db_column='pro_id')),
            ],
            options={
                'db_table': 'order',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SeatsRecord',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('seats_type', models.IntegerField(db_column='seats_type')),
                ('seats_number', models.IntegerField(db_column='seats_number')),
                ('update_time', models.DateTimeField(db_column='update_time')),
            ],
            options={
                'db_table': 'seats_record',
                'managed': False,
            },
        ),
    ]
