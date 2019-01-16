# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import FormView

# Create your views here.
def home(request):
    return render(request, 'simulation/home.html')