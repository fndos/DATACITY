# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.conf import settings
from simulation.forms import *
from simulation.models import *

from .. utils import copy_csv_gauging

@login_required(login_url='noAccess')
def LogisticaCreate(request):
	if request.method == 'POST' and request.FILES['file']:
		print "Se cargo un archivo"
		file = request.FILES['file']
		copy_csv_gauging(file, request.user)
		return HttpResponseRedirect('/data/')
	return render(request, 'main/logistica/form.html')

class LogisticaList(ListView):
	queryset = Logistica.objects.order_by('id')
	template_name = 'main/logistica/list.html'

class LogisticaUpdate(UpdateView):
	model = Logistica
	form_class = LogisticaForm
	template_name = 'main/logistica/form.html'
	success_url = reverse_lazy('logistica_list')

	def form_valid(self, form):
		form.instance.user =  self.request.user.id
		return super(LogisticaUpdate, self).form_valid(form)

class LogisticaDelete(DeleteView):
	model = Logistica
	template_name = 'main/logistica/delete.html'
	success_url = reverse_lazy('logistica_list')

class LogisticaShow(DetailView):
	model = Logistica
	template_name = 'main/logistica/show.html'
