from django.conf.urls import url
from search.views import search_layer,search_series,categories_json

urlpatterns =[
	url(r'^layers/$', search_layer),
	url(r'^series/$',search_series),
	url(r'^categories/$', categories_json),
]
