from django.conf.urls import url
from .views import *

urlpatterns =[
    url(r'^$', home, name='home'),
    url(r'^(?P<value>\d+)$', display_graph, name='display_graph'),
    url(r'^api/sample_count_by_month$', sample_count_by_month, name='sample_count_by_month'),
    url(r'^api/get_graph_data/(?P<value>\d+)$', get_graph_data, name='get_graph_data'), # Value debe ser cambiado por el ID
]
