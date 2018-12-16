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

class UserCreate(CreateView):
	model = User
	template_name = 'main/user/form.html'
	form_class = UserForm
	success_url = reverse_lazy('user_list')

	def form_valid(self, form):
		form.instance.created_by =  str(self.request.user)
		return super(UserCreate, self).form_valid(form)

class UserList(ListView):
	queryset = User.objects.order_by('id')
	template_name = 'main/user/list.html'

class UserUpdate(UpdateView):
	model = User
	form_class = UserForm
	template_name = 'main/user/form.html'
	success_url = reverse_lazy('user_list')

	def form_valid(self, form):
		form.instance.updated_by = str(self.request.user)
		return super(UserUpdate, self).form_valid(form)

class UserDelete(DeleteView):
	model = User
	template_name = 'main/user/delete.html'
	success_url = reverse_lazy('user_list')

class UserShow(DetailView):
	model = User
	template_name = 'main/user/show.html'
