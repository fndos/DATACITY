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
		simulation_instance =form.save(commit=False)
		simulation_instance.user = self.request.user
		simulation_instance.save()

		for f in self.request.FILES.getlist('file'):
			try:
				file_instance = SimulationFile(simulation=simulation_instance, file=f)
				file_instance.save()
			except Exception:
				pass

		return super(SimulationCreate, self).form_valid(form)

class SimulationList(TemplateView):
    template_name = 'simulation/list.html'

    def get_context_data(self, **kwargs):
        context = super(SimulationList, self).get_context_data(**kwargs)
        try:
            context['object_list'] = Simulation.objects.filter(user=self.request.user).order_by('id')
        except Simulation.DoesNotExist:
            context['object_list'] = None
        return context

class SimulationUpdate(UpdateView):
	model = Simulation
	form_class = SimulationForm
	template_name = 'simulation/form.html'
	success_url = reverse_lazy('simulation_list')

	def form_valid(self, form):
		simulation_instance =form.save(commit=False)
		simulation_instance.user = self.request.user
		simulation_instance.save()

		for f in self.request.FILES.getlist('file'):
			try:
				file_instance = SimulationFile(simulation=simulation_instance, file=f)
				file_instance.save()
			except Exception:
				pass

		return super(SimulationUpdate, self).form_valid(form)

class SimulationDelete(DeleteView):
	model = Simulation
	template_name = 'simulation/delete.html'
	success_url = reverse_lazy('simulation_list')

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
		TRACE_PATH = MEDIA + "output/resclima_trace_output.xml"
		EMISSION_PATH = MEDIA + "output/resclima_emission_output.xml"

		SUMMARY_DICT = summary_parser(SUMMARY_PATH)
		AVG_EMISSION_DICT, AVG_WEIGTH_EMISSION_DICT, AVG_LIGHT_EMISSION_DICT, KEY_VALUE_WEIGHT_MEAN_SPEED_DICT, KEY_VALUE_LIGHT_MEAN_SPEED_DICT, KEY_VALUE_WEIGHT_WAITING_DICT, KEY_VALUE_LIGHT_WAITING_DICT = emission_parser(EMISSION_PATH)
		AVG_TRACE_DICT_PESADO, AVG_TRACE_DICT_LIVIANO = trace_parser(TRACE_PATH)
		# Save to DB the Output (Usar try, except)
		try:
			output_instance = Output(simulation=Simulation.objects.get(id=pk),
				summary=SUMMARY_DICT,
				avg_trace=AVG_TRACE_DICT_PESADO,
				avg_trace_liviano=AVG_TRACE_DICT_LIVIANO,
				avg_emission=AVG_EMISSION_DICT,
				avg_weight_emission=AVG_WEIGTH_EMISSION_DICT,
				avg_light_emission=AVG_LIGHT_EMISSION_DICT,
				key_value_weight_mean_speed=KEY_VALUE_WEIGHT_MEAN_SPEED_DICT,
				key_value_light_mean_speed=KEY_VALUE_LIGHT_MEAN_SPEED_DICT,
				key_value_weight_waiting=KEY_VALUE_WEIGHT_WAITING_DICT,
				key_value_light_waiting=KEY_VALUE_LIGHT_WAITING_DICT)
			output_instance.save()
		except Exception:
			pass
		context = {}
		# Se envia el contexto para presentar un resumen breve de la simulacion
		context['simulation_summary'] = SUMMARY_DICT
		context['simulation_emission'] = AVG_EMISSION_DICT
		context['simulation_trace'] = AVG_TRACE_DICT_PESADO
		context['simulation_trace_liviano'] = AVG_TRACE_DICT_LIVIANO

	except ImportError:
		context = {}

	return render(request, 'simulation/output.html', context)
