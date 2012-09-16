from django import template
from django.core.urlresolvers import reverse
from django.middleware.csrf import get_token
from datebook import models, forms
from django.utils import simplejson

from django.conf import settings
STATIC_URL = settings.STATIC_URL


register = template.Library()

@register.inclusion_tag('datebook/fullcalendar.html', takes_context = True)
def fullcalendar_datebook(context, datebook_id):
	return configure_fullcalendar(context, datebook_id, False)

@register.inclusion_tag('datebook/fullcalendar.html')
def fullcalendar_datebook_editable(datebook_id):
	return configure_fullcalendar(datebook_id, True)


@register.inclusion_tag('datebook/fullcalendar_js.html')
def fullcalendar_js():
	return { 'STATIC_URL': STATIC_URL, }

@register.inclusion_tag('datebook/fullcalendar_css.html')
def fullcalendar_css():
	return { 'STATIC_URL': STATIC_URL, }


def configure_fullcalendar(datebook_id, editable):
	event_form = forms.EventModelForm()
	series_form = forms.SeriesModelForm()
	page_data = {
		'create_url': reverse("event_create"),
		'update_url': reverse("event_update"),
		'delete_url': reverse("event_delete"),
		'event_data_url':	reverse("event_data"),
		'event_form_url': 	reverse("event_form_html"),
		'series_form_url': 	reverse("series_form_html"),
		'datebook_id': datebook_id,
	}

	fullcalendar_options = {
		'header': {
			'left': 'prev,next today',
			'center': 'title',
			'right': 'month,agendaWeek,agendaDay'
		},
		'events': reverse("datebook_events", kwargs={'datebook_id': datebook_id, }),
		'theme': True,
		'editable': editable,
		'selectable': editable,
		'selectHelper': editable,
		'allDaySlot': True,
		'slotMinutes': 30,
	}

	return { 
		'page_data': simplejson.dumps(page_data), 
		'fullcalendar_options': simplejson.dumps(fullcalendar_options),
		'event_form': event_form,
		'series_form': series_form,
	}

