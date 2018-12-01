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
from main.views import customer, researcher, manager
from django.contrib.auth.views import logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    ############################# LOGIN REDIRECT ###############################
	url(r'^$', home, name="home"),
	url(r'^login/$', login, name="login"),
	url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
	url(r'^noAccess/$', noAccess, name="noAccess"),
	url(r'^get-task-info/',get_task_info,name="taskInfo"),
    ################################# CUSTOMER #################################
    url(r'^customer/profile/$', customer.Profile.as_view(), name='customer_profile'),
    ################################ RESEARCHER ################################
    url(r'^researcher/profile/$', researcher.Profile.as_view(), name='researcher_profile'),
    ################################# MANAGER ##################################
    url(r'^manager/profile/$', manager.Profile.as_view(), name='manager_profile'),
    url(r'^manager/user/create/$', manager.UserCreate.as_view(), name='user_create'),
    url(r'^manager/user/$', manager.UserList.as_view(), name='user_list'),
    url(r'^manager/user/update/(?P<pk>\d+)/$', manager.UserUpdate.as_view(), name='user_update'),
    url(r'^manager/user/delete/(?P<pk>\d+)/$', manager.UserDelete.as_view(), name='user_delete'),
    url(r'^manager/user/show/(?P<pk>\d+)/$', manager.UserShow.as_view(), name='user_show'),
    ################################# RESCLIMA #################################
	url(r'^admin/', include(admin.site.urls)),
	url(r'^search/', include("search.urls")),
	url(r'^layer/', include("layer.urls")),
	url(r'^vector/', include("vectorLayers.urls")),
	url(r'^series/', include("timeSeries.urls")),
	url(r'^raster/', include("rasterLayers.urls")),
	url(r'^tms/', include("tms.urls")),
]

urlpatterns += staticfiles_urlpatterns()
