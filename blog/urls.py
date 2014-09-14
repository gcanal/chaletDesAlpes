
from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
    url(r'^accueil/$', 'home'),
    url(r'^addArticle/$', 'addArticle'),
    url(r'^addCategory/$', 'addCategory'),
	url(r'^page/(\w+)/$','page'),
	url(r'^modifyArticleText/(\w+)/$','modifyArticleText'),
	url(r'^modifyArticleImage/(\w+)/$','modifyArticleImage'),
	url(r'^deleteArticle/(\w+)/$','deleteArticle'),
	url(r'^deleteCategory/(\w+)/$','deleteCategory'),
	url(r'^renameCategory/(\w+)/$','renameCategory'),
	url(r'^deleteCategoryWithConfirmation/(\w+)/$','deleteCategoryWithConfirmation'),
	

)

#	url(r'^modifyNouvelleText/(?P<idNouvelle>\d+)/(?P<lan>\S+)/$', 'modifyNouvelleText'),
#	url(r'^deleteNouvelle/(?P<idNouvelle>\d+)/$', 'deleteNouvelle'),
#	url(r'^modifyNouvelleImage/(?P<idNouvelle>\d+)/$', 'modifyNouvelleImage'),
#	url(r'^createNouvelle/$', 'createNouvelle'),
#	url(r'^read/(?P<idArticle>\d+)/$', 'read'), 

