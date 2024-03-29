# Generated by Django 4.1.7 on 2023-07-23 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snh48', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performancesong',
            options={'managed': False, 'verbose_name': '公演歌曲', 'verbose_name_plural': '公演歌曲'},
        ),
        migrations.CreateModel(
            name='PerformanceSongPerformances',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snh48.performance')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snh48.performancesong')),
            ],
            options={
                'verbose_name': '公演&歌曲映射',
                'verbose_name_plural': '公演&歌曲映射',
                'db_table': 'performance_song_performance',
                'managed': True,
            },
        ),
    ]
