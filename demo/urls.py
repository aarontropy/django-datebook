from django.conf.urls import patterns, include, url
from datebook import urls as datebook_urls
from demo import views



urlpatterns = patterns('',
	url(r'^datebook/',									include(datebook_urls)),
	url(r'^(?P<datebook_id>\d+)/',						views.datebook_view, name='datebook_view'),
	url(r'^test/', views.test_view),
	url(r'^', 											views.index, name='index'),

)
