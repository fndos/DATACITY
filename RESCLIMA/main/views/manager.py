# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import *

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .. decorators import *
from .. forms import *
from .. models import *

@method_decorator([login_required(login_url='noAccess'), manager_required], name='dispatch')
class Profile(TemplateView):
	template_name = 'main/manager/profile.html'

@method_decorator([login_required(login_url='noAccess'), manager_required], name='dispatch')
class UserCreate(CreateView):
	model = User
	template_name = 'main/manager/user/form.html'
	form_class = UserForm
	success_url = reverse_lazy('user_list')

	def form_valid(self, form):
		form.instance.created_by =  str(self.request.user)
		return super(UserCreate, self).form_valid(form)

@method_decorator([login_required(login_url='noAccess'), manager_required], name='dispatch')
class UserList(ListView):
	queryset = User.objects.order_by('id')
	template_name = 'main/manager/user/list.html'

@method_decorator([login_required(login_url='noAccess'), manager_required], name='dispatch')
class UserUpdate(UpdateView):
	model = User
	form_class = UserForm
	template_name = 'main/manager/user/form.html'
	success_url = reverse_lazy('user_list')

	def form_valid(self, form):
		form.instance.updated_by = str(self.request.user)
		return super(UserUpdate, self).form_valid(form)

@method_decorator([login_required(login_url='noAccess'), manager_required], name='dispatch')
class UserDelete(DeleteView):
	model = User
	template_name = 'main/manager/user/delete.html'
	success_url = reverse_lazy('user_list')

@method_decorator([login_required(login_url='noAccess'), manager_required], name='dispatch')
class UserShow(DetailView):
	model = User
	template_name = 'main/manager/user/show.html'
