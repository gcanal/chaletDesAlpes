#-*- coding: utf-8 -*-
from __future__ import unicode_literals # default encoding type is unicode like in python 3
#in python 2 legacy, s="this a bytestring(utf-8)"; s=u"this is unicode"
#in python 3, s=b"this is a bytestring(utf-8)";s="this is unicode"
from django.forms.formsets import formset_factory
from django import forms
from website.models import Section
from django.contrib.auth.models import User
import random
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from captcha.fields import CaptchaField #check if installed

#forms for the application website

class SectionForm(forms.Form):
	titre=forms.CharField(label="Titre", max_length=80,required=False)
	pageId= forms.ChoiceField(label="Page de la section",widget=forms.Select(),choices=((0, 'Accueil'),(1, 'Appartement Djan é Glyâmo'),(2, 'Appartement Mestyé'),(3, 'Appartement Martnà'),(4, 'Plus du chalet'),(5, 'Cote cosy'),(6, 'À proximité'),(7, 'Pour venir au chalet'),(8,'Réservation'),(9, 'Contact')),)
	position=forms.CharField(label="Position", max_length=80)
	#sectionNumber=forms.CharField(label="Numero de section", max_length=2)
	paragraphe=forms.CharField(label="paragraphe", widget=forms.Textarea, max_length=10000,required=False)
	image=forms.ImageField(required=False)
	legende=forms.CharField(label="Legende", max_length=80,required=False)
	link=forms.CharField(label="lien",max_length=100,required=False)
	linkText=forms.CharField(label="texte du lien",max_length=100,required=False)
	
	#regles de validation
	def clean_pageId(self):
		pageId=self.cleaned_data['pageId']
		correct=False
		try: 
			a=int(pageId)
			if a>=0 and a<10:
				correct=True
		except ValueError:
			correct=False
		if (correct==False):
			raise forms.ValidationError("Le champ numero de section doit etre un entier compris entre 0 et 9")
		return pageId
		
class SectionForm2(forms.Form):
	#each field is not required to create a section.
	#Only the pageId and the position in the page matter
	titre=forms.CharField(label="Titre", max_length=80,required=False)
	paragraphe=forms.CharField(label="paragraphe", widget=forms.Textarea, max_length=10000,required=False)
	image=forms.ImageField(required=False)
	legende=forms.CharField(label="Legende", max_length=80,required=False)
	link=forms.CharField(label="lien",max_length=100,required=False)
	linkText=forms.CharField(label="texte du lien",max_length=100,required=False)
			
class SectionTextForm(forms.Form):
	titre=forms.CharField(label="Titre", max_length=80,required=False)
	paragraphe=forms.CharField(label="paragraphe", widget=forms.Textarea, max_length=10000,required=False)
	legende=forms.CharField(label="Legende", max_length=80,required=False)
	link=forms.CharField(label="lien",max_length=100,required=False)
	linkText=forms.CharField(label="texte du lien",max_length=100,required=False)
	def __init__(self, *args, **kwargs):
		titreInit=kwargs.pop('titre','')
		legendeInit=kwargs.pop('legende','')
		paragrapheInit=kwargs.pop('paragraphe','')
		linkInit=kwargs.pop('link','')
		linkTextInit=kwargs.pop('linkText','')
		#'titre' is passed to __init__ so it's defined outside of it
		#hence the if titreInit
		super(SectionTextForm, self).__init__(*args, **kwargs)
		if titreInit:
			self.fields['titre'].initial=titreInit
		if legendeInit:
			self.fields['legende'].initial=legendeInit
		if paragrapheInit:
			self.fields['paragraphe'].initial=paragrapheInit
		if linkInit:
			self.fields['link'].initial=linkInit	
		if linkTextInit:
			self.fields['linkText'].initial=linkTextInit		

#user_details is passed to __init__, so is not defined outside of it. 
#That's why you can't access it when you're instatiating that CharField object.

class SectionImageForm(forms.Form):
	image=forms.ImageField(required=False,label="image")
	
class ConnexionForm(forms.Form):
	username = forms.CharField(label="Nom d'utilisateur", max_length=30)
	password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
	
	
class CalendarSetUpForm(forms.Form):
    lastDate = forms.DateField(required=False,label="date De fin du calendrier ",widget=forms.TextInput(attrs={'id' : 'lastDate'}));
    action= forms.ChoiceField(label="Action",widget=forms.Select(),choices=((1, 'verrouiller'),(-1, 'déverouiller')),)
    startDate= forms.DateField(required=False,label="Début de la période",widget=forms.TextInput(attrs={'id' : 'startDate'}));
    endDate= forms.DateField(required=False,label="Fin de la période",widget=forms.TextInput(attrs={'id' : 'endDate'}));
    
    
    def clean(self):
        cleaned_data = super(CalendarSetUpForm, self).clean()
        startDate = cleaned_data.get("startDate")
        endDate = cleaned_data.get("endDate")
        if startDate and endDate:
            if startDate > endDate:
				raise forms.ValidationError("Erreur : la date de fin doit être supérieure à la date de début" )
        if startDate:
			if not endDate:
				raise forms.ValidationError("Une date est manquante");
        if endDate:
			if not startDate:
				raise forms.ValidationError("Une date est manquante");
        return cleaned_data;

def create_label(n1,n2):
	lab='';
	if translation.get_language() == 'fr':
		lab='si on ajoute '+ str(n1)+' à '+str(n2)+', le résultat est';
	else:
		lab='if we add '+ n1+' to '+n2+', the result is ';
	return lab;
		#self.fields['captcha']=forms.IntegerField(label=lab,required=True);

class ContactForm(forms.Form):
	purpose=forms.ChoiceField(label=_("Vous voulez"),widget=forms.Select(),choices=((1, _("Faire une demande de réservation")),(0, _("Écrire un poème"))),);
	firstName=forms.CharField(label=_("Prénom (facultatif)"),required=False,max_length=100);
	lastName=forms.CharField(label=_("Nom (facultatif)"),required=False,max_length=100);
	appartementSelection=forms.ChoiceField(label=_("Appartement "),widget=forms.Select(),choices=((1,_(u"Djan é Glyâmo")),(3, _(u"Martnà"))),);
	startDate= forms.DateField(required=False,label=_("Début de la période"),widget=forms.TextInput(attrs={'id' : 'startDate'}));
	endDate= forms.DateField(required=False,label=_("Fin de la période"),widget=forms.TextInput(attrs={'id' : 'endDate'}));
	subject = forms.CharField(label=_("Sujet (facultatif)"),required=False,max_length=100);
	message = forms.CharField(label=_("Message"), widget=forms.Textarea, max_length=10000,required=True)
	sender = forms.EmailField(label=_("Votre email s'il vous plaît "),);
	cc_myself = forms.BooleanField(label=_("Reçevoir un copie du mail"),required=False);
	#n1 = User.objects.make_random_password(length=5, allowed_chars='123456789');n11=int(n1);
	#n2 = User.objects.make_random_password(length=1, allowed_chars='123456789');n22=int(n2);
	#captcha = forms.IntegerField(label=create_label(n1,n2),required=True);
	captcha2 = CaptchaField(label=_("Êtes-vous un robot ?"));
	

#	def clean_captcha(self):
#		captcha=self.cleaned_data['captcha']
#		correct=False;
#		a=int(self.n1)+int(self.n2);b=int(captcha);
#		print(a);print(b);
#		try: 
#			if (a == b):
#				correct=True;
#		except ValueError:
#			correct=False
#		if(not correct):
#			self.random_generation();
#		return captcha
#   def random_generation(self):
#        self.n1 = User.objects.make_random_password(length=5, allowed_chars='123456789');self.n11=int(self.n1);
#        self.n2 = User.objects.make_random_password(length=1, allowed_chars='123456789');self.n22=int(self.n2);	"

 
class ArticleCounterForm(forms.Form):
	counter=forms.IntegerField(required=True,label="nombre d'articles ",max_value= 100);
	
	


