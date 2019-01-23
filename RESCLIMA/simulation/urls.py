from django.conf.urls import url
from .views import *

urlpatterns =[
    url(r'^create/$', SimulationCreate.as_view(), name='simulation_create'),
    url(r'^$', SimulationList.as_view(), name='simulation_list'),
    url(r'^update/(?P<pk>\d+)/$', SimulationUpdate.as_view(), name='simulation_update'),
    url(r'^delete/(?P<pk>\d+)/$', SimulationDelete.as_view(), name='simulation_delete'),
    url(r'^run/(?P<pk>\d+)/$', SimulationRun.as_view(), name='simulation_run'),
    url(r'^run/(?P<pk>\d+)/output/$', SimulationOutput, name='simulation_output'), 
]
