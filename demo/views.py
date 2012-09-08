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