from django.conf.urls import url
from timeSeries.views import *

urlpatterns = [
	url(r'^$',home, name="ts_home"),
	url(r'^import/station/$', import_station, name="ts_importstation"),
	url(r'^import/file/$', import_file, name="ts_importfile"),
	url(r'^view/$', visualize, name="ts_visualize"),
	url(r'^variable/info/(?P<variable_id>\w+)/$',get_variable_info,name="get_variable_info"),
	url(r'^measurements/$', get_measurements, name="ts_measurements"),
	url(r'^measurements/download/$', download_measurements, name="ts_download_measurements"),
]
