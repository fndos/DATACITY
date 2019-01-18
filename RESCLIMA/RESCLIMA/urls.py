"""RESCLIMA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from main.views import *
from main.views import manager
from django.contrib.auth.views import logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .api import router

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ############################# LOGIN REDIRECT ###############################
	url(r'^$', home, name="home"),
	url(r'^login/$', login, name="login"),
	url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^auth_logout/$', logout, {'next_page': '/'}, name='auth_logout'),
	url(r'^noAccess/$', noAccess, name="noAccess"),
	url(r'^get-task-info/',get_task_info,name="taskInfo"),
    url(r'^profile/$', profile, name='profile'),
    url(r'^products/$', products, name='products'),
    ################################# MANAGER ##################################
    url(r'^user/create/$', manager.UserCreate.as_view(), name='user_create'),
    url(r'^user/$', manager.UserList.as_view(), name='user_list'),
    url(r'^user/update/(?P<pk>\d+)/$', manager.UserUpdate.as_view(), name='user_update'),
    url(r'^user/delete/(?P<pk>\d+)/$', manager.UserDelete.as_view(), name='user_delete'),
    url(r'^user/show/(?P<pk>\d+)/$', manager.UserShow.as_view(), name='user_show'),
    ################################# RESCLIMA #################################
	url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
	url(r'^search/', include("search.urls")),
	url(r'^layer/', include("layer.urls")),
	url(r'^vector/', include("vectorLayers.urls")),
	url(r'^series/', include("timeSeries.urls")),
	url(r'^raster/', include("rasterLayers.urls")),
	url(r'^tms/', include("tms.urls")),
    url(r'^simulation/', include("simulation.urls")),
    url(r'^d3/', include('d3.urls')),
    url(r'^dashboard/', include('dash.urls')),
    url(r'^dashboard/', include('dash.contrib.apps.public_dashboard.urls')),
]

urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
