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
from nouvelles.models import Nouvelle
from website.models import Section, Profil, CalendarLockParams, LockedDate,LockedPeriod, Message,NouvelleCounter
from nouvelles.forms import NouvelleForm
from website.forms import SectionForm,SectionForm2, SectionTextForm, SectionImageForm, ConnexionForm, CalendarSetUpForm, ContactForm
from website.forms import NouvelleCounterForm
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.core.mail import send_mail , BadHeaderError
from django.utils import translation
#fromchaletDesAlpes.context_processors import view_name_context_processor
from django.template import RequestContext
#from django.utils.translation import ugettext as _#for i18n
import locale
from django.utils.encoding import smart_text
from django.conf import settings
#from django.contrib.gis.utils import GeoIP # for ip geo-localization
from django.contrib.gis.geoip import GeoIP
from visites.models import Visitor


def activate(request, lan,pageId):
	translation.activate(lan);
	return redirect(view_from_pageId(pageId))
	
def render_from_pageId(request,pageIdAsked):
	pageId=int(pageIdAsked)
	nouvelleCounter, created = NouvelleCounter.objects.get_or_create(pageId=pageId,defaults={'counter': 3})
	sections=Section.objects.filter(pageId=pageIdAsked).order_by('position');
	nouvellesSection=Nouvelle.objects.filter(nouvellePageId=pageIdAsked)
	dernieresNouvelles=Nouvelle.objects.order_by('-date')[:nouvelleCounter.counter]# latest Nouvelle Objects limitated to "counter"
	#nNouvelles=min(dernieresNouvelles.count(),counter);#number of news that will be displayed on the page	
	
	return render(request, pageIdToTemplate(pageIdAsked),locals(),context_instance=RequestContext(request))

def home(request):
	#we record the ip adress for our visit counter
	g = GeoIP()
	ip = request.META.get('REMOTE_ADDR', None);country="";city="";
	print ip;
	if ip:
		if g.city(ip):
			city = g.city(ip)['city'];
			country=g.city(ip)['country_name'];
		if country==None or country=="":
			country="inconnu"
		if city==None or city=="":
			city="inconnu"
		visitor,info = Visitor.objects.get_or_create(ip=ip,city=city,country=country,defaults={'visitCounter': 0});
		visitor.update();
	return render_from_pageId(request,0)
	
	
def appartementDjanEGlyamo(request):
	return render_from_pageId(request,1)
def appartementMestye(request):
	return render_from_pageId(request,2)
def appartementMartna(request):
	return render_from_pageId(request,3)
def plusDuChalet(request):
	return render_from_pageId(request,4)
def coteCosy(request):
	return render_from_pageId(request,5)
def aProximite(request):
	return render_from_pageId(request,6)
def pourVenir(request):
	return render_from_pageId(request,7)

def nouvelleCounter(request,pageIdAsked):
	pageIdAsked=int(pageIdAsked);
	NouvelleCounterDisplay=True;#for the template
	pageName=pageIdToString(pageIdAsked);
	nouvelleCounter,info=NouvelleCounter.objects.get_or_create(pageId=pageIdAsked,defaults={'counter': 5})
	pageId=17;
	if request.method=='POST':
		form=NouvelleCounterForm(request.POST)
		if form.is_valid():
			counter=form.cleaned_data['counter'];
			nouvelleCounter.counter=counter;
			nouvelleCounter.save(update_fields=['counter'])
			return redirect(view_from_pageId(pageIdAsked))
	else:
		form=NouvelleCounterForm(initial={'counter': nouvelleCounter.counter,},);
	return render(request, 'website/websiteFormTemplate.html',locals())
	

def contact(request):
	pageId=9;
	#Params for the calendar
	lastDateDjanEGlyamo=datetime.today();
	lastDateMartna=datetime.today();
	try:
		lockParamsDjanEGlyamo=CalendarLockParams.objects.get(appartId=1)#get return an object
		lastDateDjanEGlyamo=lockParamsDjanEGlyamo.lastDate;
		lockParamsMartna=CalendarLockParams.objects.get(appartId=3)#get return an object
		lastDateMartna=lockParamsMartna.lastDate;
	except Exception:
		lastDateDjanEGlyamo=datetime.today();
	lockedDatesDjanEGlyamo=LockedDate.objects.filter(appartId=1);
	lockedDatesMartna=LockedDate.objects.filter(appartId=3);
	success=False;# to inform the template
	#the following has to be improved using a context-template
	nouvelleCounter, created = NouvelleCounter.objects.get_or_create(pageId=pageId,defaults={'counter': 3})
	sections=Section.objects.filter(pageId=pageId).order_by('position');
	nouvellesSection=Nouvelle.objects.filter(nouvellePageId=pageId)
	dernieresNouvelles=Nouvelle.objects.order_by('-date')[:nouvelleCounter.counter]# latest Nouvelle Objects limitated to "counter"
	form = ContactForm(request.POST or None, request.FILES or None)
	if request.method == 'POST': # If the form has been submitted...
		if form.is_valid(): # All validation rules pass
			purpose=form.cleaned_data['purpose'];firstName=form.cleaned_data['firstName'];lastName=form.cleaned_data['lastName'];
			startDate=form.cleaned_data['startDate'];endDate=form.cleaned_data['endDate'];subject=form.cleaned_data['subject'];
			message=form.cleaned_data['message'];sender=form.cleaned_data['sender'];cc_myself=form.cleaned_data['cc_myself'];
			appartementSelection=form.cleaned_data['appartementSelection'];
			appartString="";
			#
			print "purpose"
			print purpose;
			if appartementSelection == '1':
				#print "\n you chose DjanEGlyamo\n ";
				appartString="Djan é Glyâmo";
			if appartementSelection ==  '3':
				appartString="Martnà";				
			note=" via www.chalet-djan-e-glyamo.eu] ";
			subject=note+subject;
			messageType="";	
			m1="";nameGiven="";
			m1+="\n******************** Contact ********************\n"+sender;
			if translation.get_language() == 'fr':
				if purpose=='1':
					m1+="\n\n************** Dates sélectionnées **************\n";
					messageType="[Demande de résevation";
					if (startDate and endDate):
						locale.setlocale(locale.LC_ALL, b"fr_FR.UTF-8");
						#m1+="from : "+startDate.strftime("%d (%A)/%m (%B)/%Y")+"\n";
						#m1+="to   : "+endDate.strftime("%d (%A)/%m (%B)/%Y")+"\n";
						m1+="début : "+smart_text(startDate.strftime("%A %d %B %Y"), encoding='utf-8',)+"\n";
						m1+="fin   : "+smart_text(endDate.strftime("%A %d %B %Y"), encoding='utf-8',)+"\n";
					else:
						m1+="Pas de dates sélectionnées \n"
					m1+="\n************ Appartement sélectionné *************\n"+"Appartement "+appartString;
					m1+="\n\n******************** Message ********************\n";
				else:
					messageType="[Poème";
					m1+="\n******************** Message ********************\n"
				if (firstName or lastName):
					nameGiven=" de "+firstName+" "+lastName;
			else: #language='en'
				if purpose=='1':
					messageType="[Booking request";
					m1+="\n\n**************** Selected dates *****************\n"
					if (startDate and endDate):
						locale.setlocale(locale.LC_ALL, b"en_US.UTF-8");
						m1+="from : "+startDate.strftime("%d (%A)/%m (%B)/%Y")+"\n";
						m1+="to   : "+endDate.strftime("%d (%A)/%m (%B)/%Y")+"\n";
					else:
						m1+="You didn't choose any dates \n"
					m1+="\n************** Apartment selected ***************\n"+"Apartment "+appartString+' \n';
					m1+="\n\n******************** Message ********************\n"
				else:
					messageType="[Poem";
					m1+="\n******************** Message ********************\n"
				if (firstName or lastName):
					nameGiven=" from "+firstName+" "+lastName;				
			message=m1+message;
			subject=messageType+nameGiven+subject;
			success=True;
			#print subject;
			#print message;
			recipients = settings.EMAIL_RECIPIENTS;
			from_adress=settings.FROM_ADRESS;
			send_mail(subject=subject, message=message, from_email=from_adress, recipient_list=recipients,fail_silently=True);
			# if the user requested a copy of the e-mail, we send it to him (alone)
			if cc_myself:
				recipients=[];
				recipients.append(sender);
				send_mail(subject=subject, message=message, from_email=from_adress, recipient_list=recipients,fail_silently=True);
			#return HttpResponseRedirect('website.views.home')
	return render(request, 'website/contact.html',locals())




@permission_required("perms.website.add_section")
def creationSection(request,lan):
	#creation of a section 
	dernieresNouvelles=Nouvelle.objects.order_by('-date')
	pageId=10;
	if request.method=='POST':
		form=SectionForm(request.POST,request.FILES)
		if form.is_valid():
			titre=form.cleaned_data['titre'];pageId=form.cleaned_data['pageId'];paragraphe=form.cleaned_data['paragraphe']
			legende=form.cleaned_data['legende'];position=form.cleaned_data['position'];image=form.cleaned_data['image']
			envoi=True
			#creation of the section object
			#A section is always created in fr
			section=Section(titre_fr=titre,pageId=pageIdAsked,paragraphe_fr=paragraphe,legende_fr=legende,image=image,position=positionAsked,translated=False,modifiedInFr=True)
			sectionsFor=Section.objects.filter(pageId=pageIdAsked)
			for s in sectionsFor:
					if s.position >= positionAsked:
						s.set_position(s.position+1)
						s.save(update_fields=['position'])
			section.save() # we save the section object after the loop so that its section number is not incremented
			return redirect(view_from_pageId(pageId))
	else:
		displayForm=True;
		form=SectionForm()
	return render(request, 'website/websiteFormTemplate.html',locals())

@permission_required("perms.website.add_section")
def creationSectionId(request,pageIdAsked,positionAsked):
	#creation of a section knowing the page  Id
	dernieresNouvelles=Nouvelle.objects.order_by('-date')
	pageId=11;	
	positionAsked=int(positionAsked)
	if request.method=='POST':
		form=SectionForm2(request.POST,request.FILES)#form without pageId or pagePosition request.FILES because a picture is uploaded
		if form.is_valid():
			titre=form.cleaned_data['titre'];paragraphe=form.cleaned_data['paragraphe'];legende=form.cleaned_data['legende'];
			image=form.cleaned_data['image'];link=form.cleaned_data['link'];linkText=form.cleaned_data['linkText'];
			#a section is always created in fr
			section=Section(titre_fr=titre,pageId=pageIdAsked,paragraphe_fr=paragraphe,legende_fr=legende,image=image,link=link,linkText_fr=linkText,position=positionAsked,translated=False,modifiedInFr=True)
			# we increment position's attributes of the sections on the same page
			sectionsFor=Section.objects.filter(pageId=pageIdAsked)
			for s in sectionsFor:
					if s.position >= positionAsked:
						s.set_position(s.position+1)
						s.save(update_fields=['position'])
			section.save() # we save the section object after the loop so that its section number is not incremented
			return redirect(view_from_pageId(pageIdAsked))
	else:
		form=SectionForm2()
		displayForm=True;
		return render(request, 'website/websiteFormTemplate.html',locals())

@permission_required("perms.website.delete_section")		
def deleteSection(request,pageIdAsked,positionAsked): #deletes the section of the given pageId in the given position
	pageId=12
	sec=Section.objects.filter(pageId=pageIdAsked).filter(position=positionAsked)
	sec.delete()
	sectionsFor=Section.objects.filter(pageId=pageIdAsked)
	positionAsked=int(positionAsked)
	for s in sectionsFor:
		if s.position > positionAsked:
			s.set_position(s.position-1)
			s.save(update_fields=['position'])
	#redirecting to the previous page		
	return redirect(view_from_pageId(pageIdAsked))
	

@permission_required("perms.website.change_section")		
def modifySectionText(request,pageIdAsked,positionAsked,lan):#modifies the section of the given pageId in the given position
	pageId=13;textModification=True;
	sec=Section.objects.get(pageId=pageIdAsked,position=positionAsked)#get return an object , filter a queryset
	if request.method=='POST':
		form=SectionTextForm(request.POST)
		if form.is_valid():
			titre=form.cleaned_data['titre'];paragraphe=form.cleaned_data['paragraphe'];legende=form.cleaned_data['legende'];
			link=form.cleaned_data['link'];linkText=form.cleaned_data['linkText'];
			if lan=='fr':
				sec.titre_fr=titre;sec.paragraphe_fr=paragraphe;sec.legende_fr=legende;sec.modifiedInFr=True;
				sec.linkText_fr=linkText;sec.link=link;
				sec.save(update_fields=['titre_fr','paragraphe_fr','legende_fr','modifiedInFr','link','linkText_fr'])
			else:#lan='en'
				sec.titre_en=titre;sec.paragraphe_en=paragraphe;sec.legende_en=legende;sec.modifiedInFr=False;sec.translated=True;
				sec.linkText_en=linkText;sec.link=link;
				sec.save(update_fields=['titre_en','paragraphe_en','legende_en','modifiedInFr','translated','link','linkText_en'])			
			#redirecting to the startpage
			return redirect(view_from_pageId(pageIdAsked))
	else:#Get method
		displayForm=True;
		if lan == 'fr':
			form=SectionTextForm(titre=sec.titre_fr,paragraphe=sec.paragraphe_fr,legende=sec.legende_fr,link=sec.link,linkText=sec.linkText_fr);
		else:
			form=SectionTextForm(titre=sec.titre_en,paragraphe=sec.paragraphe_en,legende=sec.legende_en,link=sec.link,linkText=sec.linkText_en)	 
		return render(request,'website/websiteFormTemplate.html',locals())
	 
@permission_required("perms.website.change_section")	 
def modifySectionImage(request,pageIdAsked,positionAsked):	 
	pageId=14;imageModification=True # flag for the template
	sec=Section.objects.get(pageId=pageIdAsked,position=positionAsked)#get return an object , filter a queryset
	if request.method=='POST':
		form=SectionImageForm(request.POST,request.FILES)
		if form.is_valid():
			image=form.cleaned_data['image']
			sec.image=image;sec.save(update_fields=['image'])
			return redirect(view_from_pageId(pageIdAsked))#redirecting to the startpage
	else:
		displayForm=True;
		form=SectionImageForm()	 
		return render(request,'website/websiteFormTemplate.html',locals())

def reservations(request):
	#here the use of simplejson might be needed : from django.utils import simplejson ; blajs=simplejson.dumps(blapy);
	ip= (u"Votre IP est %s") % request.META['REMOTE_ADDR'];
	pageId=8;
	lastDateDjanEGlyamo=datetime.today();
	lastDateMartna=datetime.today();
	try:
		lockParamsDjanEGlyamo=CalendarLockParams.objects.get(appartId=1)#get return an object
		lastDateDjanEGlyamo=lockParamsDjanEGlyamo.lastDate;
		lockParamsMartna=CalendarLockParams.objects.get(appartId=3)#get return an object
		lastDateMartna=lockParamsMartna.lastDate;
	except Exception:
		lastDateDjanEGlyamo=datetime.today();
	lockedDatesDjanEGlyamo=LockedDate.objects.filter(appartId=1);
	lockedDatesMartna=LockedDate.objects.filter(appartId=3);
	
	nouvelleCounter, created = NouvelleCounter.objects.get_or_create(pageId=pageId,defaults={'counter': 3})
	sections=Section.objects.filter(pageId=pageId).order_by('position');
	nouvellesSection=Nouvelle.objects.filter(nouvellePageId=pageId)
	dernieresNouvelles=Nouvelle.objects.order_by('-date')[:nouvelleCounter.counter]# latest Nouvelle Objects limitated to "counter"
	return render(request, 'website/reservations.html' ,locals())

@permission_required("perms.website.add_lockedDate",)
def calendrier(request,appartId):
	pageId=15;
	if int(appartId)==1:
		pageId=16;
	appartId=int(appartId);
	lockedDates=LockedDate.objects.filter(appartId=appartId);
	try:
		lockParams=CalendarLockParams.objects.get(appartId=appartId)#get return an object , filter a queryset
	except Exception:
		lockParams=CalendarLockParams(appartId=appartId,lastDate=datetime.today());#we use it for the very first time
		lockParams.save();
	lastDate=lockParams.lastDate;
	calendarSetup=True;
	#view to setup the calendars (change availibilities ,...)
	#appartId=3 for Martna ; appartId=1 for DjanEGlyamo ; 
	if request.method=='POST':
		form=CalendarSetUpForm(request.POST)
		if form.is_valid():
			startDate=form.cleaned_data['startDate'];
			lastDate=form.cleaned_data['lastDate'];
			endDate=form.cleaned_data['endDate'];
			action=form.cleaned_data['action'];action=int(action);
			lockParams.setLastDate(lastDate);
			if (startDate and endDate):
				if endDate >= startDate:
					d = startDate;
					delta = timedelta(days=1);
					while d <= endDate:
						if action==1:#lock Mode
							lockParams.addLockedDate(d);
						else:#unlockMode
							lockParams.deleteLockedDate(d);
						d += delta;
			lockParams.save();
	else:
		form=CalendarSetUpForm(initial={'lastDate': lastDate,},);
	return render(request, 'website/websiteFormTemplate.html',locals())


def connexion(request):
	pageId=17;
	authentification=True;error = False;
	if request.method == "POST":
		form = ConnexionForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]  
			password = form.cleaned_data["password"] 
			user = authenticate(username=username, password=password)
			if user:  
				login(request, user)  
			else:
				error = True
	else:
		form = ConnexionForm()
	return render(request, 'website/websiteFormTemplate.html',locals())                                                      
                                                                                                        
def deconnexion(request): 
	pageId=17;                                                                              
	logout(request)                                                                                     
	return redirect('website.views.home')	
	
def pageIdToString(pageId):
	if isinstance( pageId, int ):
		pageId=str(pageId)
	if pageId=='0':
		return "HomePage"
	if pageId=='1':
		return "Appartement DjanEGlyamo"
	if pageId=='2':
		return "Appartement Mestye"
	if pageId=='3':
		return "Appartement Martna"
	if pageId=='4':
		return "Plus du chalet"
	if pageId=='5':
		return "Cote cosy"
	if pageId=='6':
		return "A proximite"
	if pageId=='7':
		return "Pour venir"
	if pageId=='8':
		return "Reservation"
	if pageId=='9':
		return "Contact"
	if pageId=='10':
		return "Page Creation Section"
	if pageId=='11':
		return "page Creation de section avec Id"
	return "undefined pageId"

def pageIdToTemplate(pageId):
	if isinstance( pageId, int ):
		pageId=str(pageId)
	if pageId=='0':
		return 'website/home.html'
	if pageId=='1':
		return 'website/appartementDjanEGlyamo.html'
	if pageId=='2':
		return 'website/appartementMestye.html'
	if pageId=='3':
		return 'website/appartementMartna.html'
	if pageId=='4':
		return 'website/plusDuChalet.html'
	if pageId=='5':
		return 'website/coteCosy.html'
	if pageId=='6':
		return 'website/aProximite.html'
	if pageId=='7':
		return 'website/pourVenir.html'
	if pageId=='8':
		return 'website/reservations.html'
	if pageId=='9':
		return 'website/contact.html'
	else :
		return 'website/home.html'
		
viewsFromId={0: 'website.views.home',1: 'website.views.appartementDjanEGlyamo',2:'website.views.appartementMestye',
3:'website.views.appartementMartna',4:'website.views.plusDuChalet',5:'website.views.coteCosy',6:'website.views.aProximite',
7:'website.views.pourVenir',8:'website.views.reservations',9:'website.views.contact'}

def view_from_pageId(pageId):
	pageId=int(pageId)
	return viewsFromId[pageId]#.get(pageId, default='website.views.home')

