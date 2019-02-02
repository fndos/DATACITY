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
from .. utils import copy_csv_clima

@login_required(login_url='noAccess')
def ClimaCreate(request):
	if request.method == 'POST' and request.FILES['file']:
		file = request.FILES['file']
		copy_csv_clima(file, request.user)
		return HttpResponseRedirect('/clima/')
	return render(request, 'main/clima/form.html')


class ClimaList(TemplateView):
    template_name = 'main/clima/list.html'

    def get_context_data(self, **kwargs):
        context = super(ClimaList, self).get_context_data(**kwargs)
        try:
            context['object_list'] = Clima.objects.filter(user=self.request.user).order_by('id')
        except Clima.DoesNotExist:
            context['object_list'] = None
        return context

# No se esta usando por el momento
class ClimaUpdate(UpdateView):
	model = Clima
	form_class = ClimaForm
	template_name = 'main/clima/form.html'
	success_url = reverse_lazy('clima_list')

	def form_valid(self, form):
		form.instance.user =  self.request.user.id
		return super(ClimaUpdate, self).form_valid(form)

# No se esta usando por el momento
class ClimaDelete(DeleteView):
	model = Clima
	template_name = 'main/clima/delete.html'
	success_url = reverse_lazy('clima_list')

# No se esta usando por el momento
class ClimaShow(DetailView):
	model = Clima
	template_name = 'main/clima/show.html'
