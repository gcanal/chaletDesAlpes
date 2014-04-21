#-*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max,Min
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
# Models for the application website


class Section(models.Model):
    titre_fr = models.CharField(max_length=100)
    titre_en= models.CharField(max_length=100)
    paragraphe_en=models.TextField(null=True)
    paragraphe_fr=models.TextField(null=True)
    legende_en=models.TextField(null=True)
    legende_fr=models.TextField(null=True)
    pageId=models.PositiveIntegerField()
    image=models.ImageField(upload_to='imagesSections/')
    position=models.PositiveIntegerField()
    link=models.CharField(max_length=1000);
    linkText_fr=models.CharField(max_length=1000);
    linkText_en=models.CharField(max_length=1000);
    translated=models.BooleanField();
    modifiedInFr=models.BooleanField(); 
    
    def set_position(self,pos):
		self.position=pos;
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
    def titre(self):
		if get_language() == 'fr':
			return self.titre_fr;
		else:
			return self.titre_en;
			
    @property
    def linkText(self):
		if get_language() == 'fr':
			return self.linkText_fr;
		else:
			return self.linkText_en;
							
    def __unicode__(self):
		return u"%s" % self.titre			

class Profil(models.Model):
    user = models.OneToOneField(User)
    isColumnist=models.BooleanField(default=False)
    inscrit_newsletter = models.BooleanField(default=False)
    def __unicode__(self):
        return u"Profil de {0}".format(self.user.username)
        
class CalendarLockParams(models.Model):
	appartId=models.PositiveSmallIntegerField();#1 for Djan, 2 for Glyamo, 3 for Martna
	lastDate=models.DateField(auto_now=False, auto_now_add=False);
	
	def setLastDate(self,newLastDate):
		if newLastDate==self.lastDate:
			return
		#we have to update the locked dates that might be  after the new last date
		upDates=LockedDate.objects.filter(appartId=self.appartId).filter(date__gt=newLastDate);#order_by("date")
		for lockedDate in upDates:
			lockedDate.delete();
		self.lastDate=newLastDate;
		self.save(update_fields=['lastDate']);
		
	def addLockedDate(self,date):
		# before we add a new lockedDate we check if it does not already exist and if it is below the lastDate attribute
		try:
			lockedDate1=LockedDate.objects.get(appartId=self.appartId,date=date)#get return an object , filter a queryset
			return;#if it already exists, there is nothing to add
		except Exception:
			if (date<self.lastDate):
				#we create a new LockedDate object
				lockedDate=LockedDate(date=date,appartId=self.appartId);
				lockedDate.save();
				
	def deleteLockedDate(self,date):
		try:
			lockedDate1=LockedDate.objects.get(appartId=self.appartId,date=date)#get return an object , filter a queryset
			lockedDate1.delete();
		except Exception:
			#nothing to delete because the locked date doesn' exist
			return;
			
	def update(self):
		today=datetime.today();
		lockedDates=LockedDate.objects.filter(appartId=self.appartId);
		for lockedDate in lockedDates:
			if lockedDate.date < today:
				lockedDate.delete();
				
	def addLockedPeriod(self,start,end):#assuming that start <=end
		#if the period turns out to be inside an already existing period, we do noting 
		lockedPeriods0=LockedPeriod().objects.filter(appartId=self.appartId).filter(startDate__lt=start).filter(endDateDate__gt=end);
		if lockedPeriods0:
			return;
		lockedPeriods1=LockedPeriod().objects.filter(appartId=self.appartId).filter(startDate__gt=start).filter(startDate__lt=end);
		endMax=datetime.today();
		if lockedPeriods1:
			endMax=lockedPeriods1.aggregate(Max(endDate));
			lockedPeriods1.delete();
			endMax=max(endMax,end);
		else:
			endMax=end;
		lockedPeriods2=LockedPeriod().objects.filter(appartId=self.appartId).filter(endDate__gt=start).filter(endDate__lt=end);
		startMin=datetime.today();
		if lockedPeriods2:
			startMin=lockedPeriods2.aggregate(Min(startDate));
			lockedPeriods2.delete();
			startMin=min(startMin,start);
		else:
			startMin=start;
		newLockedPeriod=LockedPeriod(appartId=self.appartId,startDate=startMin,endDate=endMax);
		newLockedPeriod.save();
		self.mergePeriods();
			
	def addUnLockedPeriod(self,start,end):#assuming that start <=end
		lockedPeriods1=LockedPeriod().objects.filter(appartId=self.appartId).filter(startDate__gt=start).filter(startDate__lt=end);
		for p in lockedPeriods1:
			if p.endDate <= end:
				p.delete(); 
			else:
				p.startDate=end+timedelta(days=1);p.save(update=['startDate']);
		lockedPeriods2=LockedPeriod().objects.filter(appartId=self.appartId).filter(endDate__gt=start).filter(endDate__lt=end);
		for p in lockedPeriods2:
			if p.startDate >= start	:
				p.delete();
			else:
				p.endDate=start-timedelta(days=1);p.save(update=['endDate']);
		lockedPeriods3=LockedPeriod().objects.filter(appartId=self.appartId).filter(startDate__gt=start).filter(startDate__lt=end);
		#gt means > gte means >=
		for p in lockedPeriods3:#if p exists, it is unique
			newP=LockedPeriod(appartId=self.appartId,startDate=p.startDate,endDate=start-timedelta(days=1));newP.save();
			p.startDate=end-timedelta(days=1);p.save(update=['startDate']);
		self.mergePeriods();	
			
	def mergePeriods(self):
		lockedPeriods=LockedPeriod().objects.filter(appartId=self.appartId);
		again=True;
		while again:
			again=False;
			for p in lockedPeriods:
				try:
					p2=lockedPeriods.get(startDate=p.endDate+timedelta(days=1));
					again=True;
					p.endDate=p2.endDate;p.save(update=['endDate']);p2.delete();
					lockedPeriods=LockedPeriod().objects.filter(appartId=self.appartId);
					break;# we go over the lockedPeriods again (-1) until we don't find any tangential periods.
				except Exception:
					again=False;		
			
class LockedDate(models.Model):
	appartId=models.PositiveSmallIntegerField();#1 for DjanEGlyamo, 2 for Mestye, 3 for Martna
	date=models.DateField(auto_now=False, auto_now_add=False);

class LockedPeriod(models.Model):
	appartId=models.PositiveSmallIntegerField();#1 for DjanEGlyamo, 2 for Mestye, 3 for Martna
	startDate=models.DateField(auto_now=False, auto_now_add=False);
	endDate=models.DateField(auto_now=False, auto_now_add=False);
    
class Message(models.Model):
	messageType=models.BooleanField()# 1 for a booking request 0 for a plain message
	startDate= models.DateField();
	endDate= models.DateField();
	endDate= models.DateField();
	appartementSelected=models.CharField(max_length=100);
	firstName=models.CharField(max_length=100);
	lastName=models.CharField(max_length=100);
	subject = models.CharField(max_length=100);
	message = models.TextField(null=True);
	sender = models.EmailField();
	cc_myself = models.BooleanField();
    
class NouvelleCounter(models.Model):
	pageId=models.PositiveSmallIntegerField();
	counter=models.PositiveSmallIntegerField();
	
