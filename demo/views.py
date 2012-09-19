from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse


from datebook.forms import EventModelForm
from datebook.models import Datebook

def index(request):
	datebooks = Datebook.objects.all()
	template = 'demo/index.html'
	data = {
		'datebooks': datebooks,
	}
	return render_to_response( template, data, context_instance = RequestContext(request))

def datebook_view(request, datebook_id):
	"""
	
	"""
	template = 'datebook/datebook_view.html'
	data = {
		'datebook_id': datebook_id,
	}
	return render_to_response( template, data, context_instance = RequestContext(request))

def test_view(request):
	from datebook.forms import TestForm, TestModelForm
	from datetime import datetime, timedelta
	from dateutil import parser

	# parser.parse(init['start']) - timedelta(minutes=int(init['offset'])) 
	d = parser.parse(u"2012-09-11T04:00:00.000Z") - timedelta(minutes=u'240')
	init = {'start': d, 'end': d}
	form = TestForm(initial=init)
	modelform = EventModelForm(initial=init)
	template = 'datebook/test_template.html'
	
	data = {
		'form': form,
		'modelform': modelform,
	}
	return render_to_response( template, data, context_instance = RequestContext(request))