from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
# Create your models here

class Event(models.Model):
	eventId = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 200)
	durationInMins = models.IntegerField()
	def __unicode__(self):
		return self.name



class Set(models.Model):
	setId = models.AutoField(primary_key = True)
	setname = models.CharField(max_length = 200)
	numberOfQuestions = models.IntegerField()
	test = models.ForeignKey(Event)
	positiveMarks = models.PositiveIntegerField()
	negativeMarks = models.PositiveIntegerField()
	def __unicode__(self):
		return "Set name : "+self.setname+" Event : "+self.test.name



class Questions(models.Model):
	question = models.CharField(max_length = 1000)
	answer = models.CharField(max_length = 1000)
	option_B = models.CharField(max_length = 1000)
	option_C = models.CharField(max_length = 1000)
	option_D = models.CharField(max_length = 1000)
	set = models.ForeignKey(Set)
	def __unicode__(self):
		return self.question
	@classmethod
	def create(cls,question,answer,optionB,optionC,optionD,set):
		question = cls(question = question,answer = answer,option_B = optionB,option_C=optionC,option_D = optionD,set = set)
		return question



class Score(models.Model):
	user = models.ForeignKey(User)
	event =  models.ForeignKey(Event)
	score = models.IntegerField(blank=True,null=True)
	startTime = models.DateTimeField(blank=True,null=True)
	negatives = models.PositiveIntegerField(blank = True,null = True)
	deltaSec = models.PositiveIntegerField(blank=True,null=True)
	deltaMicro =  models.PositiveIntegerField(blank=True,null=True)
	def __unicode__(self):
		return "User : "+self.user.username+" Event : "+self.event.name
	@classmethod
	def create(cls,user,event):
		score = cls(user = user , event = event)
		return score

admin.site.register(Event)
admin.site.register(Set)
admin.site.register(Questions)
admin.site.register(Score)
