from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from exam.models import Event
class Volunteer(models.Model):
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	def __unicode__(self):
		return "User name : "+self.user.username+" Event: "+self.event.name
admin.site.register(Volunteer)
