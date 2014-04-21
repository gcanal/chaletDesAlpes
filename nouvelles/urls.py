
from django.conf.urls import patterns, include, url
from nouvelles.forms import NouvelleForm
urlpatterns = patterns('nouvelles.views',
    url(r'^accueil/$', 'homeNouvelles'),
	url(r'^read/(?P<idNouvelle>\d+)/$', 'read'), 
	url(r'^modifyNouvelleText/(?P<idNouvelle>\d+)/(?P<lan>\S+)/$', 'modifyNouvelleText'),
	url(r'^deleteNouvelle/(?P<idNouvelle>\d+)/$', 'deleteNouvelle'),
	url(r'^modifyNouvelleImage/(?P<idNouvelle>\d+)/$', 'modifyNouvelleImage'),
	url(r'^createNouvelle/$', 'createNouvelle'),
)
