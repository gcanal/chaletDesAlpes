#-*- coding: utf-8 -*-
from django import forms
from django.forms.formsets import formset_factory
from blog.models import Category
import re
#forms for the application website

class ArticleForm(forms.Form):
	# see http://stackoverflow.com/questions/5708650/how-do-i-add-a-foreign-key-field-to-a-modelform-in-django
	#nouvellePageId= forms.ChoiceField(label="Choix de la section",widget=forms.Select(),choices=((0, 'HomePage'),(1, 'Appartement Djan'),(2, 'Appartement Glyamo'),(3, 'Appartement Martna'),(4, 'Plus du chalet'),(5, 'Cote cosy'),(6, 'A proximite'),(7, 'Pour venir au chalet'),(8,'Reservation'),(9, 'Contact')),)
	category = forms.ModelChoiceField(queryset = Category.objects.all() )
	title=forms.CharField(label="Titre", max_length=80,required=True)
	summary=forms.CharField(label="Resume", max_length=80,required=False)
	paragraph=forms.CharField(label="Contenu", widget=forms.Textarea, max_length=2000,required=False)
	image=forms.ImageField(required=False)
	caption=forms.CharField(label="légende",max_length=100,required=False)
	link=forms.CharField(label="lien",max_length=100,required=False)
	linkText=forms.CharField(label="texte du lien",max_length=100,required=False)

class ArticleTextForm(forms.Form):
	title=forms.CharField(label="Titre", max_length=80,required=False)
	paragraph=forms.CharField(label="paragraphe", widget=forms.Textarea, max_length=10000,required=False)
	caption=forms.CharField(label="Legende", max_length=80,required=False)
	link=forms.CharField(label="lien",max_length=100,required=False)
	linkText=forms.CharField(label="texte du lien",max_length=100,required=False)
	def __init__(self, *args, **kwargs):
		titleInit=kwargs.pop('title','')
		captionInit=kwargs.pop('caption','')
		paragraphInit=kwargs.pop('paragraph','')
		linkInit=kwargs.pop('link','')
		linkTextInit=kwargs.pop('linkText','')
		super(ArticleTextForm, self).__init__(*args, **kwargs)
		if titleInit:
			self.fields['title'].initial=titleInit
		if captionInit:
			self.fields['caption'].initial=captionInit
		if paragraphInit:
			self.fields['paragraph'].initial=paragraphInit
		if linkInit:
			self.fields['link'].initial=linkInit	
		if linkTextInit:
			self.fields['linkText'].initial=linkTextInit		

class ArticleImageForm(forms.Form):
	image=forms.ImageField(required=True);

	
class CategoryForm(forms.Form):
	title=forms.CharField(label="Nom de la categorie", max_length=80,required=True)
	#regles de validation
	def clean_title(self):
		title=self.cleaned_data['title']
		t1=re.sub(r'[^a-zA-Z0-9]',' ', title)#removing all non alphanumeric char from the string
		#comparing 
		categories=Category.objects.all();
		for cat in categories:
			t2=re.sub(r'[^a-zA-Z0-9]',' ', cat.title);
			if (t1 == t2):
				raise forms.ValidationError("Cette categorie existe déjà")
		return title

"""	


		lockParams=CalendarLockParams.objects.get(appartId=appartId)
		title=self.cleaned_data['title']
		t1=re.sub(r'[^a-zA-Z0-9]',' ', title)#removing all non alphanumeric char from the string
		#comparing 
		categories=Category.objects.all();
		correct=True
		for cat in categories:
			t2=re.sub(r'[^a-zA-Z0-9]',' ', cat.title);
			if (t1 == t2):
				raise forms.ValidationError("Cette section existe déjà")
		return title



	#regles de validation
	def clean_sectionNumber(self):
		sectionNumber=self.cleaned_data['sectionNumber']
		correct=False
		try: 
			a=int(sectionNumber)
			if a>0 and a<10:
				correct=True
		except ValueError:
			correct=False
		if (correct==False):
			raise forms.ValidationError("Le champ numero de section doit etre un entier compris entre 1 et 9")
		return sectionNumber

	
class EnTeteForm(forms.Form):
	titre=forms.CharField(label="Titre", max_length=80)
	sectionNumber= forms.ChoiceField(label="Choix de la section",widget=forms.Select(),choices=((1, 'Appartement Djan'),(2, 'Appartement Glyamo'),(3, 'Appartement Martna'),(4, 'Plus du chalet'),(5, 'Cote cosy'),(6, 'A proximite'),(7, 'Pour venir au chalet'),(8,'Reservation'),(9, 'Contact')),)
	#sectionNumber=forms.CharField(label="Numero de section", max_length=2)
	contenu=forms.CharField(label="Contenu", widget=forms.Textarea, max_length=2000)
	n=forms.CharField(label="Nombre de sections", max_length=1)#nombre de sections supplementaires.
	#regles de validation
	def clean_sectionNumber(self):
		sectionNumber=self.cleaned_data['sectionNumber']
		correct=False
		try: 
			a=int(sectionNumber)
			if a>0 and a<10:
				correct=True
		except ValueError:
			correct=False
		if (correct==False):
			raise forms.ValidationError("Le champ numero de section doit etre un entier compris entre 1 et 9")
		return sectionNumber
		
	def clean_n(self):
		n=self.cleaned_data['n']
		correct=False
		try: 
			a=int(n)
			if a>0 and a<10:
				correct=True
		except ValueError:
			correct=False
		if (correct==False):
			raise forms.ValidationError("Le champ numero de section doit etre un entier compris entre 1 et 9")
		return n		
				
class SectionSupplementaireForm(forms.Form):
			contenuSection=forms.CharField(label="Contenu de la section", widget=forms.Textarea, max_length=2000)	
				
			
class SectionsSupplementaireForm(forms.Form):
    def __init__(self,*args,**kwargs):
		n= kwargs.pop('n', 0)
		super(SectionsSupplementaireForm, self).__init__(*args, **kwargs)
		for index in range(n):
            # generate extra fields in the number specified via extra_fields
			self.fields['texte_{index}'.format(index=index)]=forms.CharField()			
		
class MyForm(forms.Form):
    original_field = forms.CharField()
    extra_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields

        for index in range(extra_fields):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_field_{index}'.format(index=index)] = \
                forms.CharField()			
"""		

