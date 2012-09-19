from django import forms
from django.utils import timezone
from django.utils.formats import get_format
from django.utils.safestring import mark_safe

from django.forms.widgets import SplitDateTimeWidget


from datetime import datetime
import dateutil.parser

from datebook import models as datebook

import logging
log = logging.getLogger('app')

DATE_FORMAT = '%A, %b %d, %Y'
TIME_FORMAT = '%I:%M %p'

class DatePickerWidget(forms.widgets.Widget):
	def render(self, name, value, attrs=None):
		if value is None:
			vstr = ''
		elif hasattr(value, 'strftime'):
			vstr = value.strftime(DATE_FORMAT)
		else:
			# This is a string, so try to parse it in ISO format and then format it properly
			try:
				vdate = dateutil.parser.parse(value)
				vstr = vdate.strftime(DATE_FORMAT)
			except:
				vstr = value
		id = "id_%s" % name
		args = [
			"<input class=\"datepicker\" type=\"text\" value=\"%s\" name=\"%s\" id=\"%s\" readonly=\"true\" />" % \
			(vstr, name, id),
			"<script type=\"text/javascript\">$(\"#%s\").datepicker({dateFormat:'DD, M d, yy'}).datepicker('setDate', '%s');</script>" % (id, vstr,)
			]
		return mark_safe("\n".join(args))


class TimePickerWidget(forms.widgets.Widget):
	def render(self, name, value, attrs=None):
		if value is None:
			vstr = ''
		elif hasattr(value, 'strftime'):
			vstr = value.strftime(TIME_FORMAT)
		else:
			# This is a string, so try to parse it in ISO format and then format it properly
			try:
				vdate = dateutil.parser.parse(value)
				vstr = vdate.strftime(TIME_FORMAT)
			except:
				vstr = value
		id = "id_%s" % name
		args = [
			"<input class=\"timepicker\" type=\"text\" value=\"%s\" name=\"%s\" id=\"%s\" readonly=\"true\" />" % (vstr, name, id),
			"<script type=\"text/javascript\">$(\"#%s\").timepicker({showLeadingZero: false, showPeriod: true, minutes: { interval: 15} }).timepicker('setTime', '%s');</script>" % (id, vstr,)
			]
		return mark_safe("\n".join(args))


class JqDateTimeWidget(forms.widgets.MultiWidget):
	def __init__(self, attrs=None):
		widgets = [
			DatePickerWidget(),
			TimePickerWidget()
			# forms.widgets.TextInput({'class': 'datePicker', 'readonly':'true'}),
			# forms.widgets.TextInput({'class': 'timePicker', 'readonly':'true'})
		]
		super(JqDateTimeWidget, self).__init__(widgets, attrs)

	def decompress(self, value):
		""" You have to implement this method in order to subclass a MultiWidget.
		Look at django.forms.widgets.SplitDateTimeWidget for another example."""
		if value:
			return [value.date(), value.time().replace(microsecond=0),]
		return [None, None]

	def value_from_datadict(self, data, files, name):
		date_value, time_value = super(JqDateTimeWidget, self).value_from_datadict(data, files, name)
		if date_value and time_value:
			datetime_format = "%s %s" % (DATE_FORMAT, TIME_FORMAT)
			datetime_input_format = "%s %s" % (get_format('DATE_INPUT_FORMATS')[0], get_format('TIME_INPUT_FORMATS')[1])
			datetime_string = "%s %s" % (date_value, time_value)
			try:
				return datetime.strptime(datetime_string, datetime_format) .replace(tzinfo=timezone.utc) #get_current_timezone())
			except ValueError:
				return None
		return None

class WeekdayPicker(forms.widgets.MultiWidget):
	"""
	This widget should display a list of seven checkboxes corresponding to the seven days of the week 
	The values for the seven checkboxes correspond to the integer values for rrule.MO, rrule.TU, and so on
	The return value from this widget is a comma-separated list of the selected integers
	"""
	def __init__(self, attrs=None):
		widgets = [forms.CheckboxInput(),] * 7
		super(WeekdayPicker, self).__init__(widgets, attrs)

	def decompress(self, value):
		"""
		take a comma-separated list of integers (value) and return a list of booleans
		"""
		b = [False] * 7
		val = value or ''
		for i in [int(s) for s in val.split(',') if len(val)>0 ]:
			b[i] = True
		return b

	def value_from_datadict(self, data, files, name):
		"""
		Take a list of booleans and make a string representing a comma-separated integer list
		The booleans are the checkbox values and the string represents the weekdays picked (rrule.MO, etc.)
		"""
		b = super(WeekdayPicker, self).value_from_datadict(data, files, name)
		return ','.join([str(idx) for idx, day in enumerate(b) if day])




FIELD_NAME_MAPPING = {
	'title': 'event_title',
}


class EventModelForm(forms.ModelForm):
	start 		= forms.DateTimeField(widget=JqDateTimeWidget)
	end 		= forms.DateTimeField(widget=JqDateTimeWidget)
	tz 			= forms.CharField(initial='America/Louisville')
	title 		= forms.CharField(required=False)
	location 	= forms.CharField(required=False)

	datebook 	= forms.ModelChoiceField(widget=forms.HiddenInput, queryset=datebook.Datebook.objects.all())
	event 		= forms.CharField(widget=forms.HiddenInput, required=False)

	action 		= forms.CharField(initial='create', widget=forms.HiddenInput)

	
	class Meta:
		model = datebook.Event
		exclude = ['series',]

	# The overridden method is here to allow me to rename the title field.
	# I need to do this so that the event title does not conflict with the datebook
	# title on the admin page.
	def add_prefix(self, field_name):
		# look up field name; return original if not found
		field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
		return super(EventModelForm, self).add_prefix(field_name)


class SeriesModelForm(forms.ModelForm):
	day_list = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=datebook.Series.day_list_choices)

	series = forms.CharField(widget=forms.HiddenInput, required=False)

	class Meta:
		model = datebook.Series

class TestModelForm(forms.ModelForm):
	start = forms.DateTimeField(widget=JqDateTimeWidget)
	end = forms.DateTimeField(widget=JqDateTimeWidget)

	class Meta:
		model = datebook.TestModel

class TestForm(forms.Form):
	start = forms.DateTimeField(widget=JqDateTimeWidget)
	end = forms.DateTimeField(widget=SplitDateTimeWidget)

