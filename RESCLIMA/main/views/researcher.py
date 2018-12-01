# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import *

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .. decorators import *

@method_decorator([login_required(login_url='noAccess'), researcher_required], name='dispatch')
class Profile(TemplateView):
    template_name = 'main/researcher/profile.html'
