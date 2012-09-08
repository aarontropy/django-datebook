from django.conf.urls import patterns, include, url
from datebook import data_views



urlpatterns = patterns('',
	url(r'^ajax/event/create/',							data_views.event_create, 	name="event_create"),
	url(r'^ajax/event/update/',							data_views.event_update, 	name="event_update"),
	url(r'^ajax/event/delete/',							data_views.event_delete, 	name="event_delete"),
	url(r'^ajax/datebook/(?P<datebook_id>\d+)/events/',	data_views.datebook_events, name="datebook_events"),
)
