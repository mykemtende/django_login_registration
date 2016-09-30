from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	idno = models.CharField(max_length=10)
	photo = models.ImageField(upload_to='profile_photo', blank=True)
	description = models.TextField()
	def __unicode__(self):
		return self.user.username
