from django.contrib import admin

from datebook import models as datebook

class InlineEvent(admin.TabularInline):
	model=datebook.Event

class DatebookAdmin(admin.ModelAdmin):
	pass
	

admin.site.register(datebook.Datebook, DatebookAdmin)
# admin.site.register(Session, SessionAdmin)
# admin.site.register(CourseRegistration)

