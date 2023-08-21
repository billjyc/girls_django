# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Memberinfo, Team, Performance, PerformanceHistory, MemberAbility, PerformanceSong, SenbatsuElection, SenbatsuElectionDetail


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memberinfo
        fields = '__all__'


class MemberAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberAbility
        fields = '__all__'


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'

    def get_num(self, obj):
        return PerformanceHistory.objects.filter(performance=obj).count()


class PerformanceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceHistory
        fields = '__all__'


class PerformanceSongSerializer(serializers.ModelSerializer):
    song_type = serializers.IntegerField()
    rank = serializers.IntegerField()

    class Meta:
        model = PerformanceSong
        fields = ['id', 'name', 'song_type', 'rank']


class TeamSerializer(serializers.ModelSerializer):
    details = PerformanceSerializer(many=True, read_only=True, source='performance_set')

    class Meta:
        model = Team
        fields = '__all__'


class SenbatsuElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenbatsuElection
        fields = '__all__'


class SenbatsuElectionDetailSerializer(serializers.ModelSerializer):
    member_info = MemberSerializer(source='member', read_only=True)  # 添加此字段
    class Meta:
        model = SenbatsuElectionDetail
        fields = '__all__'
