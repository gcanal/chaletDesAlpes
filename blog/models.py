#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import get_language
#models for the application nouvelles

#french only in the blog section
class Article(models.Model):
	title = models.CharField(max_length=100)
	summary=models.CharField(max_length=100)
	paragraph= models.TextField(null=True)
	image=models.ImageField(upload_to='imagesBlog/',null=True,blank=True)
	caption=models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de parution")
	link=models.CharField(max_length=100)
	linkText=models.CharField(max_length=100)
	category = models.ForeignKey('Category')
	def __unicode__(self):
		return u"%s" % self.titre
	"""
	@property 
	def titre(self):
		if get_language() == 'fr':
			return self.titre_fr;
		else:
			return self.titre_en;
	@property 
	def resume(self):
		if get_language() == 'fr':
			return self.resume_fr;
		else:
			return self.resume_en;			
	@property 	
	def paragraphe(self):
		if get_language() == 'fr':
			return self.paragraphe_fr;
		else:
			return self.paragraphe_en;
	@property 
	def legende(self):
		if get_language() == 'fr':
			return self.legende_fr;
		else:
			return self.legende_en;
	@property 
	def linkText(self):
		if get_language() == 'fr':
			return self.linkText_fr;
		else:
			return self.linkText_en;
	"""

class Category(models.Model):
	title = models.CharField(max_length=100)
	
	def __unicode__(self):
		return u"%s" % self.title
	
