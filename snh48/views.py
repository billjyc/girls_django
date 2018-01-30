# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import *


# Create your views here.

def index(request):
    member_list = Memberinfo.objects.order_by('id')
    # template = loader.get_template('snh48/index.html')
    context = {
        'member_list': member_list,
    }
    return render(request, 'snh48/index.html', context)
    # return HttpResponse(template.render(context, request))


def member_detail(request, member_id):
    member = get_object_or_404(Memberinfo, pk=member_id)
    return render(request, 'snh48/member_detail.html', {'member': member})
