from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns =[
    url(r'^create/$', login_required(SimulationCreate.as_view(), login_url='noAccess'), name='simulation_create'),
    url(r'^$', login_required(SimulationList.as_view(), login_url='noAccess'), name='simulation_list'),
    url(r'^update/(?P<pk>\d+)/$', login_required(SimulationUpdate.as_view(), login_url='noAccess'), name='simulation_update'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(SimulationDelete.as_view(), login_url='noAccess'), name='simulation_delete'),
    url(r'^run/(?P<pk>\d+)/$', login_required(SimulationRun.as_view(), login_url='noAccess'), name='simulation_run'),
    url(r'^run/(?P<pk>\d+)/output/$', SimulationOutput, name='simulation_output'),
]
