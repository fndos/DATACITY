# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.edit import FormView
from django.views.generic import *

from django.conf import settings
from django.urls import reverse_lazy

from . models import *
from . forms import *
from . tasks import *
from . utils import cutter
from . parsers import (
	emission_parser,
	trace_parser,
	summary_parser
)

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
			# Utilizar cutter para crear el path de salida
			temp, cut_position, cut_user = cutter(params['simulation_whole_path'])
			params['simulation_path'] = temp[:cut_position+1]
			result = simulation_task.delay(params)
			# Creando el contexto
			context['object_list'] = Simulation.objects.filter(id=self.kwargs['pk'])
			context['task_id'] = result.task_id
		except Simulation.DoesNotExist:
			context['object_list'] = None
		return context

def SimulationOutput(request, pk):
	try:
		dict = {}
		dict['simulation_whole_path'] = Simulation.objects.get(id=pk).sumo_config.path.replace(settings.MEDIA_ROOT, '')
		# Utilizar cutter para crear el path de salida
		temp, cut_position, cut_user = cutter(dict['simulation_whole_path'])
		dict['simulation_path'] = temp[:cut_position+1]

		MEDIA = settings.MEDIA_ROOT + dict['simulation_path']

		SUMMARY_PATH = MEDIA + "output/resclima_summary_output.xml"
		TRACE_PATH = MEDIA + "output/resclima_sumo_trace.xml"
		EMISSION_PATH = MEDIA + "output/resclima_emission_output.xml"

		SUMMARY_DICT = summary_parser(SUMMARY_PATH)
		AVG_EMISSION_DICT, AVG_WEIGTH_EMISSION_DICT, AVG_LIGHT_EMISSION_DICT = emission_parser(EMISSION_PATH)
		AVG_TRACE_DICT, AVG_WEIGHT_TRACE_DICT, AVG_LIGHT_TRACE_DICT = trace_parser(TRACE_PATH)

		context = {}
		context['simulation_summary'] = SUMMARY_DICT
		context['simulation_emission'] = AVG_EMISSION_DICT
		context['simulation_trace'] = AVG_TRACE_DICT

	except ImportError:
		context = {}
		print("Sucedio un error compita :v")

	return render(request, 'simulation/output.html', context)
