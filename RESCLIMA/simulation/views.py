# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView

from django.urls import reverse_lazy
from django.views.generic import *
from . models import *
from . forms import *

# Create your views here.

# class SimulationCreate(FormView):
#
#     form_class = SimulationForm
#     success_url = reverse_lazy('simulation_list')
#     template_name = "simulation/form.html"
#
#     def form_valid(self, form):
#         form.instance.user =  self.request.user
#         form.save(commit=True)
#         return super(SimulationCreate, self).form_valid(form)

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

class SimulationBeforeRun(TemplateView):
    template_name = 'simulation/before_run.html'

    def get_context_data(self, **kwargs):
        context = super(SimulationBeforeRun, self).get_context_data(**kwargs)
        try:
            context['object_list'] = Simulation.objects.filter(id=self.kwargs['pk'])
        except Simulation.DoesNotExist:
            context['object_list'] = None
        return context

### Modificar para realizar la simulacin ###
class SimulationRun(TemplateView):
    template_name = 'simulation/run.html'

    def get_context_data(self, **kwargs):
        context = super(SimulationRun, self).get_context_data(**kwargs)
        try:
            context['object_list'] = Simulation.objects.filter(id=self.kwargs['pk'])
        except Simulation.DoesNotExist:
            context['object_list'] = None
        return context
