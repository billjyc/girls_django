# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Team)
admin.site.register(Memberinfo)
admin.site.register(Performance)
admin.site.register(PerformanceHistory)
admin.site.register(MemberPerformanceHistory)
admin.site.register(MemberPerformanceHistoryTmp)
admin.site.register(Unit)
admin.site.register(UnitHistory)


