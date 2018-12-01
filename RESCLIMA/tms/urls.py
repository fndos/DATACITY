
from django.conf.urls import url
from tms import views as tms_views

urlpatterns =[
	url(r'^$', tms_views.root), #ej "/tms" calls root()
  url(r'^(?P<version>[0-9.]+)$', tms_views.service), # ej, "/tms/1.0" calls service(version="1.0")
  url(r'^(?P<version>[0-9.]+)/' + r'(?P<rasterlayer_id>\d+)$',tms_views.tileMap), # eg, "/tms/1.0/2" calls tileMap(version="1.0", shapefile_id=2)
  url(r'^(?P<version>[0-9.]+)/' + r'(?P<rasterlayer_id>\d+)/(?P<zoom>\d+)/' + r'(?P<x>\d+)/(?P<y>\d+)\.png$', tms_views.tile), # eg, "/tms/1.0/2/3/4/5" calls tile(version="1.0", shapefile_id=2, zoom=3, x=4, y=5
]