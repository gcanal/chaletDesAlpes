
from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from website.models import Section

register = template.Library()
#To be a valid tag library, the module must contain a module-level variable named register that is a template.Library instance,
# in which all the tags and filters are registered


def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return simplejson.dumps(object)

register.filter('jsonify', jsonify)


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'actif'
    return 'inactif' 

@register.filter
def is_false(arg): 
    return arg is False
    
@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')
	
	
@register.filter
def isActive(value,arg):
	if value==arg:
		return 'actif'
	else:
		return 'inactif'
		
#returns the number of translated sections on a given page
@register.filter
def translatedSections(pageId):
	pageId=int(pageId);
	return Section.objects.filter(pageId=pageId, translated=True).count
	
@register.filter				
def pageIdToView(pageId):
	pageId=int(pageId);
	if pageId==0:
		return 'website.views.home'
	if pageId==1:
		return 'website.views.appartementDjanEGlyamo'
	if pageId==2:
		return 'website.views.appartementMestye'
	if pageId==3:
		return 'website.views.appartementMartna'		
	if pageId==4:
		return 'website.views.plusDuChalet'		
	if pageId==5:
		return 'website.views.coteCosy'		
	if pageId==6:
		return 'website.views.aProximite'		
	if pageId==7:
		return 'website.views.pourVenir'
	if pageId==8:
		return 'website.views.reservations'
	if pageId==9:
		return 'website.views.contact'
	if pageId==10:
		return 'website.views.creationSection'
	if pageId==11:
		return 	'website.views.creationSectionId'	
	if pageId==12:
		return 	'website.views.deleteSection'	
	if pageId==13:
		return 	'website.views.modifySectionText'			
	if pageId==14:
		return 	'website.views.modifySectionImage'	
	else:
		return 'website.views.home'		
				


@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    see https://djangosnippets.org/snippets/1357/
  """
  return range( value )
