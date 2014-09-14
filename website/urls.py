#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
#from website.views import NouvelleWizard
#from website.forms import SectionForm, CalendarSetUpForm
urlpatterns = patterns('website.views',
    url(r'^accueil/$', 'home'),
    url(r'^appartementdjaneglyamo/$', 'appartementDjanEGlyamo'),
    url(r'^appartementmestye/$', 'appartementMestye'),
    url(r'^appartementmartna/$', 'appartementMartna'),
    url(r'^plusduchalet/$', 'plusDuChalet'),
    url(r'^cotecosy/$', 'coteCosy'),
    url(r'^aproximite/$', 'aProximite'),
    url(r'^pourvenir/$', 'pourVenir'),
    url(r'^reservations/$', 'reservations'),
    url(r'^contact/$', 'contact'),
    url(r'^creationSection/$','creationSection'),
    url(r'^creationSectionId/(\d+)/(\d+)/$','creationSectionId'),
    url(r'^deleteSection/(\d+)/(\d+)/$','deleteSection'),
    url(r'^modifySectionText/(\d+)/(\d+)/(\S+)/$','modifySectionText'),
    url(r'^modifySectionImage/(\d+)/(\d+)/$','modifySectionImage'),
    url(r'^calendrier/(\d+)/$','calendrier'),
    url(r'^connexion/$','connexion'),
    url(r'^deconnexion/$', 'deconnexion'),
    url(r'^activate/(\S+)/(\d+)$', 'activate'),
)

#url(r'^creationNouvelle/$', NouvelleWizard.as_view([EnTeteForm, SectionsSupplementaireForm])),
#url(r'^nouvelleCounter/(\d+)/$','nouvelleCounter'),
