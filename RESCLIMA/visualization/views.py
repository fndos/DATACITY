# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.db import connections
from django.db.models import Count
from django.http import JsonResponse

from .models import Sample

# Create your views here.
def sample(request):
    return render(request, 'visualization/sample.html')

def sample_count_by_month(request):
    data = Sample.objects.all() \
        .extra(select={'month': connections[Sample.objects.db].ops.date_trunc_sql('month', 'date')}) \
        .values('month') \
        .annotate(count_items=Count('id'))
    return JsonResponse(list(data), safe=False)
