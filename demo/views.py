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
	form = EventModelForm()
	page_data = {
		'create_url': reverse("event_ajax_CRUD", kwargs={'action': 'create',}),
		'update_url': reverse("event_ajax_CRUD", kwargs={'action': 'update',}),
		'delete_url': reverse("event_ajax_CRUD", kwargs={'action': 'delete',}),
		'datebook_id': datebook_id,
	}

	template = 'datebook/datebook_view.html'
	data = {
		'page_data': simplejson.dumps(page_data),
		'event_form': form,
	}
	return render_to_response( template, data, context_instance = RequestContext(request))