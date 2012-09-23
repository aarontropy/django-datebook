from django.db import models
from django.conf import settings
from datebook.timezone_field import fields as timezone
from datetime import time, timedelta
from timezones.fields import TZDateTimeField

import pytz



class Datebook(models.Model):
	title		= models.CharField(max_length=255)

	def __unicode__(self):
		return self.title


class Series(models.Model):
	freq_choices = (
		(0,	'YEARLY'), 
		(1, 'MONTHLY'), 
		(2,	'WEEKLY'), 
		# (3,	'DAILY'), 
		# (4,	'HOURLY'), 
		# (5, 'MINUTELY'), 
		# (6, 'SECONDLY')
	)
	day_list_choices = (
		(7, 'Sun'),
		(0, 'Mon'),
		(1, 'Tue'),
		(2, 'Wed'),
		(3, 'Thu'),
		(4, 'Fri'),
		(5, 'Sat'),
	)
	day_list_choices
	datebook 		= models.ForeignKey(Datebook)

	start 			= models.DateTimeField(null=True)
	duration_min 	= models.IntegerField(default=60)
	freq 			= models.IntegerField(choices=freq_choices, default=2)
	interval 		= models.IntegerField(default=1)
	count			= models.IntegerField(null=True)
	until 			= models.DateTimeField(null=True)
	day_list		= models.CommaSeparatedIntegerField(max_length=25, blank=True)

	def __unicode__(self):
		return "Series for %s" % (self.datebook.title)

	@property 
	def rrule(self):
		# don't return a rrule which produces an infinite number of events
		if self.count is None and self.until is None:
			return rrule(rrule.DAILY, dtstart=self.start, count=1)

		# remember that if both count and until are provided, count controls
		try:
			return rrule(
				self.freq, 
				dtstart=self.start, 
				count=self.count, 
				until=self.until, 
				interval=self.interval,
				byweekday=self.day_list.split(','),
			)
		except:
			return None

	def generate_events(self):
		"""
		This method generates a list of datebook.Event objects, but does NOT save them
		"""
		event_list = []
		rr = self.rrule
		if rr:
			for ev in self.rrule:
				event = Event(
					start=ev,
					end=ev + timedelta(minutes=self.duration_min),
					datebook=self.datebook,
					series=self.id,
				)
				event_list.append(event)

		return event_list




		 

class Event(models.Model):
	title		= models.CharField(max_length=255, null=True)
	start		= TZDateTimeField() # always timezone aware, always UTC
	end			= TZDateTimeField() # always timezone aware, always UTC
	allDay 		= models.BooleanField(default=False)
	tz			= timezone.TimeZoneField(null=True)
	location	= models.CharField(max_length=255, null=True)

	datebook 	= models.ForeignKey(Datebook)
	series		= models.ForeignKey(Series, null=True)

	def save(self):
		super(Event,self).save()

	def totimezone(self, tz=None):
		if not tz:
			tz = self.tz if self.tz else pytz.timezone(settings.TIME_ZONE)
		self.start 	= self.start.astimezone(tz)
		self.end 	= self.end.astimezone(tz)
		return self

	def __unicode__(self):
		return "%s event for %s" % (self.start, self.datebook.title)


class TestModel(models.Model):
	start = TZDateTimeField()
	end = TZDateTimeField()