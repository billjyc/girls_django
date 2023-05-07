# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Memberinfo, Team


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memberinfo
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
