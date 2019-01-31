# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .. forms import *
from .. models import *
from .. utils import copy_csv_censo

@login_required(login_url='noAccess')
def CensoCreate(request):
	if request.method == 'POST' and request.FILES['file']:
		file = request.FILES['file']
		copy_csv_censo(file, request.user)
		return HttpResponseRedirect('/censo/')
	return render(request, 'main/censo/form.html')

class CensoList(ListView):
	queryset = Censo.objects.order_by('id')
	template_name = 'main/censo/list.html'

# No se esta usando por el momento
class CensoUpdate(UpdateView):
	model = Censo
	form_class = CensoForm
	template_name = 'main/censo/form.html'
	success_url = reverse_lazy('censo_list')

	def form_valid(self, form):
		form.instance.user =  self.request.user.id
		return super(CensoUpdate, self).form_valid(form)

# No se esta usando por el momento
class CensoDelete(DeleteView):
	model = Censo
	template_name = 'main/censo/delete.html'
	success_url = reverse_lazy('censo_list')

# No se esta usando por el momento
class CensoShow(DetailView):
	model = Censo
	template_name = 'main/censo/show.html'
