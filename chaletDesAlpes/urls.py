#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns #gestion des fichiers statiques en developpement
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings 
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import TemplateView # for robots.txt


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^i18n/', include('django.conf.urls.i18n')),#not  within i18n_patterns() - it needs to be language-independent 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',  content_type='text/plain')),
)

urlpatterns += i18n_patterns('',
    url(r'^accueil/$', 'website.views.home'),
    url(r'^$', 'website.views.home'),
    url(r'^website/', include('website.urls')),
    url(r'^nouvelles/', include('nouvelles.urls')),
      
)

urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)

### For developpement
if settings.DEBUG:
	#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #one possibility
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )#another possibility
   
urlpatterns += staticfiles_urlpatterns()
