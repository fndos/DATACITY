from django.conf.urls import url
from .views import *

urlpatterns =[
    url(r'^$', sample, name='index'),
    url(r'^api/sample_count_by_month', sample_count_by_month, name='sample_count_by_month'),
]
