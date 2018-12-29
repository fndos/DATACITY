from django.conf.urls import url
from .views import *

urlpatterns =[
    url(r'^api/test$', test, name='test'),
]
