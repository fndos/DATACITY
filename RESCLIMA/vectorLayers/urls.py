from django.conf.urls import url
from vectorLayers import views as vectorLayers_views

urlpatterns =[
	url(r'^$',vectorLayers_views.list_vectorlayers,name="vector_list"),
	url(r'^import$', vectorLayers_views.import_shapefile),
	url(r'^export/(?P<vectorlayer_id>\d+)$', vectorLayers_views.export_shapefile),
	url(r'^geojson/(?P<vectorlayer_id>\d+)$', vectorLayers_views.export_geojson),
	url(r'^edit/(?P<vectorlayer_id>\d+)$', vectorLayers_views.edit_vectorlayer),
	url(r'^delete/(?P<vectorlayer_id>\w+)/$$', vectorLayers_views.delete_vectorLayer, name="delete_layer"),
	# estilos
	url(r'^import_style/(?P<vectorlayer_id>\d+)$', vectorLayers_views.import_style, name="import_style"),
	url(r'^delete_style/(?P<style_id>\d+)$', vectorLayers_views.delete_style, name="delete_style"),
	url(r'^export_style/(?P<style_id>\d+)$', vectorLayers_views.export_style),
]
