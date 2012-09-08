from django import template
from django.core.urlresolvers import reverse
from datebook import models, forms
from django.utils import simplejson

from django.conf import settings
STATIC_URL = settings.STATIC_URL


register = template.Library()

@register.inclusion_tag('datebook/fullcalendar.html')
def fullcalendar_datebook(datebook_id):

	event_form = forms.EventModelForm()
	page_data = {
		'create_url': reverse("event_create"),
		'update_url': reverse("event_update"),
		'delete_url': reverse("event_delete"),
		'events_url': reverse("datebook_events", kwargs={'datebook_id': datebook_id, }),
		'datebook_id': datebook_id,
	}

	return { 
		'page_data': simplejson.dumps(page_data), 
		'event_form': event_form,
	}

@register.inclusion_tag('datebook/fullcalendar_js.html')
def fullcalendar_js():
	return { 'STATIC_URL': STATIC_URL, }

@register.inclusion_tag('datebook/fullcalendar_css.html')
def fullcalendar_css():
	return { 'STATIC_URL': STATIC_URL, }
