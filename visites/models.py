#-*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max,Min
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
# Models for the application visites




class Visitor(models.Model):
	ip=models.GenericIPAddressField();
	lastVisit=models.DateTimeField(auto_now=True, auto_now_add=True);
	#auto_now automatically set the field to now every time the object is saved.
	#auto_now_add automatically set the field to now when the object is first created.
	country=models.CharField(max_length=1000);
	city=models.CharField(max_length=1000);
	visitCounter=models.PositiveIntegerField();

	#zu tun for next version add pageId argument
	def update(self):
		#the last visit attribute is self-updated
		self.visitCounter=self.visitCounter+1;
		self.save(update_fields=['visitCounter']);
		
		
		
