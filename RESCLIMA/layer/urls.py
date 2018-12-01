from django.conf.urls import url
from layer import views as layer_views

urlpatterns =[
	url(r'^view/$', layer_views.view_layers),
	url(r'^info/(?P<id_layer>\w+)/$',layer_views.layer_info),
]

