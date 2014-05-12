#-*- coding: utf-8 -*-
from __future__ import unicode_literals # default encoding type is unicode like in python 3
#in python 2 legacy, s="this a bytestring(utf-8)"; s=u"this is unicode"
#in python 3, s=b"this is a bytestring(utf-8)";s="this is unicode"
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, date, timedelta
from django.contrib.auth import login,logout,authenticate                                                                         
from django.core.urlresolvers import reverse 
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.utils import translation
#fromchaletDesAlpes.context_processors import view_name_context_processor
from django.template import RequestContext
#from django.utils.translation import ugettext as _#for i18n
import locale
from django.utils.encoding import smart_text
from django.conf import settings
from visites.models import Visitor


#zu tun : ameliorer permission
@permission_required("perms.visites.add_visitor")
def dernieresvisites(request):
	visitors=Visitor.objects.order_by('lastVisit')[:10000]
	pageId=17;
	total=Visitor.objects.count();
	
	return render(request, 'visites/dernieresVisites.html',locals())
