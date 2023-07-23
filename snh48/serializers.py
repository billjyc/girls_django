# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Memberinfo, Team, Performance, PerformanceHistory, MemberAbility, PerformanceSong


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


class PerformanceSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceSong
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    details = PerformanceSerializer(many=True, read_only=True, source='performance_set')
    class Meta:
        model = Team
        fields = '__all__'
