from django.db import models
from django.conf import settings
from datebook.timezone_field import fields as timezone



class Datebook(models.Model):
	title		= models.CharField(max_length=255)

	def __unicode__(self):
		return self.title

class Series(models.Model):
	datebook 	= models.ForeignKey(Datebook)

	def __unicode__(self):
		return "SEries for %s" % (self.datebook.title)

class Event(models.Model):
	title		= models.CharField(max_length=255, null=True)
	start		= models.DateTimeField()
	end			= models.DateTimeField()
	tz			= timezone.TimeZoneField(null=True)

	datebook 	= models.ForeignKey(Datebook)
	series		= models.ForeignKey(Series, null=True)

	def __unicode__(self):
		return "%s event for %s" % (self.start, self.datebook.title)
