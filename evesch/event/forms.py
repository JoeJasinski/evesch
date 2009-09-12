from django.utils.translation import ugettext_lazy as _
from django import forms 
from event.models import  EventType, Event, Attendee
from org.models import Organization
from django.core.exceptions import ObjectDoesNotExist
from core.widgets import DateTimeWidget
from core.ajax_filtered_fields.forms import ManyToManyByLetter
from django.conf import settings
from euser.models import User
import datetime
import re 

from django.forms.widgets import  SplitDateTimeWidget, SplitHiddenDateTimeWidget


class Time12Field(forms.CharField):
    def clean(self, post_time):

        pa = re.compile('^\s*$')
        if pa.match(post_time):
            raise forms.ValidationError(_("Must enter a time"))
        p = re.compile('^\s*(?P<hour>\d{1,2})\:(?P<min>\d{2})\s*(?P<ap>am|pm)?\s*$', re.IGNORECASE)
        if not p.match(post_time):
            raise forms.ValidationError(_("Not a valid time"))
        m = p.search(post_time)
        hour = m.group('hour')
        try:
            hour = int(hour)
            if not ( hour >= 0 and  hour < 24 ):
                raise forms.ValidationError("Invalid Hour")
        except ValueError:
            raise forms.ValidationError("something bad happened.")

        min = m.group('min')
        try:
            min = int(min)
            if not ( min >= 0 and min < 60):
                raise forms.ValidationError("Invalid Minute")
        except ValueError:
            raise forms.ValidationError("something bad happened")

        ap = m.group('ap')
        if hour > 12:
            ap = ''
        if ap:
            # convert to 24H time else assume 24H time
            if ap.lower() == 'pm' and hour != 12:
                hour = int(hour) + 12
            elif ap.lower() == 'am' and hour == 12:
                hour = int(hour) + 12
            if hour == 24:
                hour = 0

        cleaned_time = datetime.time(hour, min)
        #cleaned_time = str(hour) + ":" + str(min)

        return cleaned_time

EMPTY_VALUES = (None, '')
class EveschSplitDateTimeField(forms.MultiValueField):
    widget = forms.widgets.SplitDateTimeWidget
    hidden_widget = forms.widgets.SplitHiddenDateTimeWidget
    default_error_messages = {
        'invalid_date': _(u'Enter a valid date.'),
        'invalid_time': _(u'Enter a valid time.'),
    }

    def __init__(self, input_date_formats=None, input_time_formats=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.DateField(input_formats=input_date_formats, error_messages={'invalid': errors['invalid_date']}),
            Time12Field( error_messages={'invalid': errors['invalid_time']}),
        )
        super(EveschSplitDateTimeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Raise a validation error if time or date is empty
            # (possible if SplitDateTimeField has required=False).
            if data_list[0] in EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_date'])
            if data_list[1] in EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_time'])
            return datetime.datetime.combine(*data_list)
        return None


class ColorField(forms.CharField):
 
    def clean(self, value):
        forms.Field.clean(self, value)
        if not value:
            raise forms.ValidationError(_('Choose a color'))
        if  len(value) != 6:
            raise forms.ValidationError(_('Must be 6 chars long'))
        
        p = re.compile('^[a-fA-F0-9]{6}$')
        if not p.match(value):
            raise forms.ValidationError(_('Must be a Hex Color value'))
        
        return value

class HourField(forms.CharField):
    
    def clean(self, value):
        forms.Field.clean(self, value)
        #self.max_length=4
        try:
            value = int(value)
        except ValueError: 
            raise forms.ValidationError(_('Must be a number'))
        #raise AssertionError(value)
        if value < -1000  or 1000 < value:
            raise forms.ValidationError(_('Number out of range.'))

        return value

class EventTypeForm(forms.ModelForm):
    type_desc = forms.CharField(widget=forms.Textarea(attrs = {'cols':'30','rows':'5'}))
    type_color = ColorField(widget=forms.TextInput(attrs={'size':'6','class':'color',}), max_length=6)
    class Meta:
        model = EventType
        exclude = ('org_name','type_hash','type_active')

    def __init__(self, current_org, *args, **kwargs):
        self._current_org = current_org
        super(EventTypeForm, self).__init__(*args, **kwargs)

    def clean_type_name(self):
        #raise forms.ValidationError(self.instance)
        type_name_input = self.cleaned_data['type_name']
        if int(EventType.objects.filter(type_name__iexact=type_name_input, org_name=self._current_org).exclude(id=self.instance.id).count() >= 1):
            raise forms.ValidationError(_("Type Name already exists."))
        return type_name_input

class EventForm(forms.ModelForm):
    event_desc = forms.CharField(
         widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
    event_type = forms.ModelChoiceField(queryset=EventType.objects.none())
    event_date = EveschSplitDateTimeField(widget=forms.SplitDateTimeWidget(time_format="%H:%M", attrs={'id':"id_event_date"}))
    event_signup_deadline = EveschSplitDateTimeField(widget=forms.SplitDateTimeWidget(time_format="%H:%M", attrs={'id':"id_event_signup_deadline"}))
    
    #event_coordinators = ManyToManyByLetter(User, field_name="username")


    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
            settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js",
            settings.MEDIA_URL + 'js/jqui/js/jquery-1.3.2.min.js',
            settings.MEDIA_URL + 'js/ajax_filtered_fields/ajax_filtered_fields.js',
        )
    
    
    def __init__(self, current_org, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["event_type"].queryset = EventType.objects.filter(org_name=current_org, type_active=True)

    class Meta:
        model = Event
        exclude = ('event_org','event_hash','event_creator_name','event_created_date','event_active',)
    
    
class EventEditForm(forms.ModelForm):

    def __init__(self, current_org, *args, **kwargs):
        super(EventEditForm, self).__init__(*args, **kwargs)
        self.fields["event_type"].queryset = EventType.objects.filter(org_name=current_org, type_active=True)

    event_desc = forms.CharField(max_length=512, widget=forms.Textarea(attrs = {'cols':'45','rows':'5'}))
    event_date =            EveschSplitDateTimeField(widget=forms.SplitDateTimeWidget(time_format='%H:%M', attrs={'id':"id_event_date"}))
    event_signup_deadline = EveschSplitDateTimeField(widget=forms.SplitDateTimeWidget(time_format='%H:%M', attrs={'id':"id_event_signup_deadline"}))

    class Meta:
        model = Event
        exclude = ('event_org','event_hash','event_creator_name','event_active',)
    
class AttendeeForm(forms.ModelForm):

    def __init__(self, current_event, *args, **kwargs):
        super(AttendeeForm, self).__init__(*args, **kwargs)
        if current_event.event_track_hours:
            self.fields['att_hours'] =  HourField(widget=forms.TextInput(attrs={'size':'5',}), max_length=5)
        if current_event.att_header_col1:
            self.fields['att_col1'] = forms.CharField(widget=forms.TextInput(attrs = {'size':'30',}), label=current_event.att_header_col1, required=current_event.att_require_col1)
        if current_event.att_header_col2:
            self.fields['att_col2'] = forms.CharField(widget=forms.TextInput(attrs = {'size':'30',}), label=current_event.att_header_col2, required=current_event.att_require_col2) 
        if current_event.att_header_col3:
            self.fields['att_col3'] = forms.CharField(widget=forms.TextInput(attrs = {'size':'30',}), label=current_event.att_header_col3, required=current_event.att_require_col3)
        if current_event.att_header_col4:
            self.fields['att_col4'] = forms.CharField(widget=forms.TextInput(attrs = {'size':'30',}), label=current_event.att_header_col4, required=current_event.att_require_col4)
        if current_event.att_header_col5:
            self.fields['att_col5'] = forms.CharField(widget=forms.TextInput(attrs = {'size':'30',}), label=current_event.att_header_col5, required=current_event.att_require_col5)
        if current_event.att_header_col6:
            self.fields['att_col6'] = forms.CharField(widget=forms.TextInput(attrs = {'size':'30',}), label=current_event.att_header_col6, required=current_event.att_require_col6)  
              
    class Meta:
        model = Attendee
        exclude = ('att_ip','att_event','att_name','att_hours','att_col1','att_col2','att_col3','att_col4','att_col5','att_col6')
        
