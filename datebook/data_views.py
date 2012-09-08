import sys
from django.http import HttpResponse
from django.utils import simplejson

from datetime import datetime, timedelta

from datebook.models import Event, Datebook
from datebook.forms import EventModelForm



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

def event_create(request):
	data = {}
	if request.is_ajax() and request.method=='POST':
		form = EventModelForm(request.POST)
		if form.is_valid():
			# try:
			# 	datebook_id = form.cleaned_data['datebook_id']
			# 	datebook = Datebook.objects.get(id=datebook_id)
			# except Datebook.DoesNotExist:
			# 	data = { 
			# 		'status': 'error',
			# 		'error': 'DoesNotExist Error', 
			# 		'message': 'Invalid Datebook id: [%s]' % (form.cleaned_data['datebook'],)
			# 	}
			# except KeyError:
			# 	data = { 
			# 		'status': 'error',
			# 		'error': 'No Datebook ID Error', 
			# 		'message': 'A Datebook ID must be passed to create an event'
			# 	}
			# else:
				# form.cleaned_data['datebook'] = datebook
				form.save()
				data = { 'status': 'success', }
		else:
			data = { 
				'status': 'error',
				'error': 'Validation Error', 
				'message': '\n'.join(["%s: %s" % (key, form.errors[key]) for key in form.errors]) 
			}
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
		if form.is_valid():
			form.save()
			data = { 'status': 'success', }
		else:
			data = { 
				'status': 'error',
				'error': 'Validation Error', 
				'message': '\n'.join(["%s: %s" % (key, form.errors[key]) for key in form.errors]) 
			}
	return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def event_delete(request):
	data = {}
	if request.is_ajax() and request.method=='POST':
		event = Event.objects.get(id=request.POST['event'])
		event.delete()
	return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def event_ajax_CRUD(request, action=''):
	act = action.lower()
	data = {
		'status': 'error',
		'error': 'No Valid Action',
		'message': "Action must be either 'create', 'update' or 'delete'",
	}
	if act == 'create':
		return event_create(request)
	elif act == 'update':
		return event_update(request)
	elif act == 'delete':
		return event_delete(request)
	else:
		return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def ajax_event_update(request, datebook_id=None):
	"""
	If a datebook_id is supplied, this will be the default datebook for added
	events.  Otherwise, a valid event object needs to be passed.
	"""

	data = {}

	if request.method == 'POST':
		try:
			if request.POST.has_key('id'):			# we are editing an existing Event
				try:
					event = Event.objects.get(id=request.POST['id'])
				except:
					event = None
				form = EventModelForm(instance=event, data=request.POST)
			else:
				form = EventModelForm(request.POST)

			if form.is_valid():
				# try to get the occurrence from the occurrence id, or create a new one with the current session id
				if form.cleaned_data['action'] == 'delete':
					try:
						event.delete()
					except Exception, e:
						data['error'] = 'Delete Error'
						data['errorMessage'] = str(e)
				else:
					
					try:
						form.save()
					except Exception, e:
						data['error'] = 'Save Error'
						data['errorMessage'] = str(e)
					else:
						data['status'] = 'success'
						data['message'] = ''
			else:
				data['error'] 	= 'Validation Error'
				data['errorMessage'] = '\n'.join(["%s: %s" % (key, form.errors[key]) for key in form.errors])
		except Exception, e:
			data['error'] = 'Other Error'
			data['errorMessage'] = str(e)
	jsondata = simplejson.dumps(data)
	return HttpResponse(jsondata, mimetype="application/json")