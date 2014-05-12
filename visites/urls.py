#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('visites.views',
    url(r'^dernieresvisites/$', 'dernieresvisites'),
) 

