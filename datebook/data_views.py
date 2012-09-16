import sys
from django.http import HttpResponse
from django.utils import simplejson

from datetime import datetime, timedelta
import dateutil.parser

from datebook.models import Event, Datebook
from datebook.forms import EventModelForm, SeriesModelForm

import logging
log = logging.getLogger('app')



def datebook_events(request, datebook_id):
	"""
	Returns json-encoded Events corresponding to the datebook_id
	If no datebook_id is supplied, it defaults to the first datebook
	"""
	try:
		events = list(Event.objects.filter(datebook=datebook_id))
	except:
		events = []

	data = []
	for event in events:
		# if the end time is earlier than the start time, that's silly...prevent that.
		# if the end time is the same as the start time, the calendar plugin freaks out...prevent that
		# don't save the end_time if it is changed. 
		if (event.end - event.start).seconds <= 0:
			event.end = event.start + timedelta(minutes=1)

		data.append({
				'event_id': event.id,
				'series_id': event.series,
				'datebook_id': event.datebook.id,
				'event_title': event.title,
				'title': event.title,
				'start': str(event.start.replace(tzinfo=event.tz)),
				'end': str(event.end.replace(tzinfo=event.tz)),
				'datebook': event.datebook.title,
				'allDay': False
			})
	jsondata = simplejson.dumps(data)
	return HttpResponse(jsondata, mimetype="application/json")

def event_form_html(request):
	data = {}
	# start and end dates are passed as ISO-formatted strings in UTC.
	# The offset in minutes is also passed. 
	init = {
		'start': dateutil.parser.parse(request.POST['start']) - timedelta(minutes=int(request.POST['offset'])),
		'end': dateutil.parser.parse(request.POST['end']) - timedelta(minutes=int(request.POST['offset'])),
	}

	event_id = request.POST['event_id'] if request.POST.has_key('event_id') else request.GET['event_id'] if request.GET.has_key('event_id') else None
	if event_id:
		try:
			event = Event.objects.get(id=event_id)
			form = EventModelForm(instance=event, initial=init)
			if form.is_valid():
				data = { 'as_table': form.as_table() }
			else:
				data = { 'error': 'Validity Errors: \n%s' % (str(form.errors),) }				
		except:
			data = { 'error': 'Could not get event id=%s' % (event_id,) }
	else:
		form = EventModelForm(initial=init)
		data = { 'as_table': form.as_table(),
			'start': request.POST['start'], }
	return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def series_form_html(request):
	data = {}
	series_id = request.POST['series_id'] if request.POST.has_key('series_id') else request.GET['series_id'] if request.GET.has_key('series_id') else None
	if series_id:
		try:
			series = Series.objects.get(id=request.POST['series_id'])
			form = SeriesModelForm(instance=series, initial=request.POST)
			data = { 'as_table': form.as_table() }
		except:
			data = { 'error': 'Could not get series id=%s' % (series_id,) }
	else:
		form = SeriesModelForm(initial=request.POST)
		data = { 'as_table': form.as_table() }
	return HttpResponse(simplejson.dumps(data), mimetype="application/json")







#-------------------------------------------------------------------------------
# EVENT VIEWS
#-------------------------------------------------------------------------------
def event_create(request):
	data = {}
	if request.is_ajax() and request.method=='POST':
		form = EventModelForm(request.POST)
		data = save_form(form)
	else:
		data = {
			'status': 'error',
			'error': 'Post Error',
			'message': 'Ajax %s, Post %s' % (request.is_ajax(), request.method,)
		}
	return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def event_update(request):
	data = {}
	if request.is_ajax() and request.method=='POST':
		event = Event.objects.get(id=request.POST['event'])
		form = EventModelForm(instance=event, data=request.POST)
		data = save_form(form)
	return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def event_delete(request):
	data = {}
	if request.is_ajax() and request.method=='POST':
		event = Event.objects.get(id=request.POST['event'])
		event.delete()
	return HttpResponse(simplejson.dumps(data), mimetype="application/json")

#-------------------------------------------------------------------------------
# SERIES VIEWS
#-------------------------------------------------------------------------------
def series_create(request):
	if request.is_ajax() and request.method=='POST':
		form = SeriesModelForm(request.POST)
		data = save_form(form)
	else:
		data = {
			'status': 'error',
			'error': 'Post Error',
			'message': 'Ajax %s, Post %s' % (request.is_ajax(), request.method,)
		}
	return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def series_update(request):
	if request.is_ajax() and request.method=='POST':
		series = Series.objects.get(id=request.POST['series'])
		form = SeriesModelForm(instance=series, data=request.POST)
		data = save_form(form)
	else:
		data = {
			'status': 'error',
			'error': 'Post Error',
			'message': 'Ajax %s, Post %s' % (request.is_ajax(), request.method,)
		}
	return HttpResponse(simplejson.dumps(data), mimetype="application/json")



#-------------------------------------------------------------------------------
def save_form(form):
	if form.is_valid():
		form.save()
		data = { 'status': 'success', }
	else:
		data = { 
			'status': 'error',
			'error': 'Validation Error', 
			'message': '\n'.join(["%s: %s" % (key, form.errors[key]) for key in form.errors]) 
		}
	return data
