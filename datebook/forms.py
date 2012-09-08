from django import forms
from django.utils import timezone
from django.utils.formats import get_format
from django.utils.safestring import mark_safe


from datetime import datetime

from datebook import models as datebook

DATE_FORMAT = '%A, %b %d, %Y'
TIME_FORMAT = '%I:%M %p'

class DatePickerWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        if value is None:
            vstr = ''
        elif hasattr(value, 'strftime'):
            vstr = datetime_safe.new_datetime(value).strftime(DATE_FORMAT)
        else:
            vstr = value
        id = "id_%s" % name
        args = [
            "<input class=\"datepicker\" type=\"text\" value=\"%s\" name=\"%s\" id=\"%s\" readonly=\"true\" />" % \
            (vstr, name, id),
            "<script type=\"text/javascript\">$(\"#%s\").datepicker({dateFormat:'DD, M d, yy'});</script>" % id
            ]
        return mark_safe("\n".join(args))


class TimePickerWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        if value is None:
            vstr = ''
        elif hasattr(value, 'strftime'):
            vstr = datetime_safe.new_datetime(value).strftime(DATE_FORMAT)
        else:
            vstr = value
        id = "id_%s" % name
        args = [
            "<input class=\"timepicker\" type=\"text\" value=\"%s\" name=\"%s\" id=\"%s\" readonly=\"true\" />" % \
            (vstr, name, id),
            "<script type=\"text/javascript\">$(\"#%s\").timepicker({showLeadingZero: false, showPeriod: true, minutes: { interval: 15} });</script>" % id
            ]
        return mark_safe("\n".join(args))


class JqDateTimeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            DatePickerWidget(),
            TimePickerWidget()
            # forms.widgets.TextInput({'class': 'datePicker', 'readonly':'true'}),
            # forms.widgets.TextInput({'class': 'timePicker', 'readonly':'true'})
        ]
        super(JqDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        """ You have to implement this method in order to subclass a MultiWidget.
        Look at django.forms.widgets.SplitDateTimeWidget for another example."""
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        date_value, time_value = super(JqDateTimeWidget, self).value_from_datadict(data, files, name)
        if date_value and time_value:
            datetime_format = "%s %s" % (DATE_FORMAT, TIME_FORMAT)
            datetime_input_format = "%s %s" % (get_format('DATE_INPUT_FORMATS')[0], get_format('TIME_INPUT_FORMATS')[1])
            datetime_string = "%s %s" % (date_value, time_value)
            try:
                return datetime.strptime(datetime_string, datetime_format) .replace(tzinfo=timezone.utc) #get_current_timezone())
            except ValueError:
                return None
        return None



FIELD_NAME_MAPPING = {
    'title': 'event_title',
}


class EventModelForm(forms.ModelForm):
    start = forms.CharField(widget=JqDateTimeWidget)
    end = forms.CharField(widget=JqDateTimeWidget)
    tz = forms.CharField(initial='America/Louisville')

    datebook = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=datebook.Datebook.objects.all())
    event = forms.CharField(widget=forms.HiddenInput, required=False)

    action = forms.CharField(initial='create', widget=forms.HiddenInput)

    
    class Meta:
        model = datebook.Event
        exclude = ['series',]

    # The overridden method is here to allow me to rename the title field.
    # I need to do this so that the event title does not conflict with the datebook
    # title on the admin page.
    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(EventModelForm, self).add_prefix(field_name)


        