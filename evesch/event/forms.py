from django.utils.translation import ugettext_lazy as _
from django import forms 
from event.models import  EventType, Event, Attendee
from org.models import Organization
from django.core.exceptions import ObjectDoesNotExist
from core.widgets import DateTimeWidget
import re 
    
class ColorField(forms.CharField):
 
    def clean(self, value):
        if not value:
            raise forms.ValidationError(_('Choose a color'))
        if  len(value) != 6:
            raise forms.ValidationError(_('Must be 6 chars long'))
        
        p = re.compile('^[a-zA-Z0-9]{6}$')
        if not p.match(value):
            raise forms.ValidationError(_('Must be a Hex Color value'))
        
        return value

class EventTypeForm(forms.ModelForm):
    type_desc = forms.CharField(widget=forms.Textarea(attrs = {'cols':'30','rows':'5'}))
    type_color = ColorField(widget=forms.TextInput(attrs={'size':'6','class':'color',}), max_length=6)
    class Meta:
        model = EventType
        exclude = ('org_name','type_hash','type_active')

class EventForm(forms.ModelForm):
    event_desc = forms.CharField(
         widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
    #TASK: fix this logic below - it should be a dynamic list box 
    event_type = forms.ModelChoiceField(queryset=EventType.objects.none())
    event_date = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget({'id':"id_event_date"}))
    event_signup_deadline = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget({'id':"id_event_signup_deadline"}))

    #forms.DateTimeField(widget=DateTimeWidget())
    
    def __init__(self, current_org, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["event_type"].queryset = EventType.objects.filter(org_name=current_org, type_active=True)

    class Meta:
        model = Event
        exclude = ('event_org','event_hash','event_creator_name','event_created_date',)
    
    
class EventEditForm(forms.ModelForm):

    def __init__(self, current_org, *args, **kwargs):
        super(EventEditForm, self).__init__(*args, **kwargs)
        self.fields["event_type"].queryset = EventType.objects.filter(org_name=current_org, type_active=True)

    event_desc = forms.CharField(max_length=512, widget=forms.Textarea(attrs = {'cols':'45','rows':'5'}))
    #event_date = forms.DateTimeField(widget=forms.TextInput(attrs = {'id':'id_event_date',}))
    event_date = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget({'id':"id_event_date"}))
    event_signup_deadline = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget({'id':"id_event_signup_deadline"}))

    class Meta:
        model = Event
        exclude = ('event_org','event_hash','event_creator_name',)
    
class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ('att_ip','att_event','att_name',)
        
