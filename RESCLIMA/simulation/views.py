# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView

from django.urls import reverse_lazy
from django.views.generic import *
from . models import *
from . forms import *
from . tasks import *

from django.conf import settings

# Create your views here.

class SimulationCreate(CreateView):
	template_name = 'simulation/form.html'
	form_class = SimulationForm
	success_url = reverse_lazy('simulation_list')

	def form_valid(self, form):
		form.instance.user =  self.request.user
		return super(SimulationCreate, self).form_valid(form)

class SimulationList(ListView):
	queryset = Simulation.objects.order_by('id')
	template_name = 'simulation/list.html'

class SimulationUpdate(UpdateView):
	model = Simulation
	form_class = SimulationForm
	template_name = 'simulation/form.html'
	success_url = reverse_lazy('simulation_list')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(SimulationUpdate, self).form_valid(form)

class SimulationDelete(DeleteView):
	model = Simulation
	template_name = 'simulation/delete.html'
	success_url = reverse_lazy('simulation_list')

### Modificar para realizar la simulacion ###
class SimulationRun(TemplateView):
	template_name = 'simulation/run.html'

	def get_context_data(self, **kwargs):
		context = super(SimulationRun, self).get_context_data(**kwargs)
		try:
			params = {}
			params['simulation_step'] = Simulation.objects.get(id=self.kwargs['pk']).step
			params['simulation_whole_path'] = Simulation.objects.get(id=self.kwargs['pk']).sumo_config.path.replace(settings.MEDIA_ROOT, '')
			# Funcion de corte START
			temp = params['simulation_whole_path']
			cut_position = 0
			for i in range(len(temp)-1):
				if temp[i] == "/":
					cut_position = cut_position + 1
					if cut_position == 4:
						cut_position = i
					if cut_position == 3:
						cut_user = i
			# Funcion de corte END
			params['simulation_path'] = temp[:cut_position+1]
			params['simulation_user_path'] = temp[:cut_user+1]
			result = simulation_task.delay(params)
			context['object_list'] = Simulation.objects.filter(id=self.kwargs['pk'])
			context['task_id'] = result.task_id

		except Simulation.DoesNotExist:
			context['object_list'] = None
		return context
