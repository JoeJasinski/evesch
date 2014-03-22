import datetime
import re 
from django.utils.translation import ugettext_lazy as _
from django import forms 
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from evesch.event.models import  EventType, Event, Attendee
from evesch.org.models import Organization
from evesch.core.widgets import DateTimeWidget
from evesch.core.ajax_filtered_fields.forms import ManyToManyByLetter


from django.forms.widgets import  SplitDateTimeWidget, SplitHiddenDateTimeWidget

class ColorField(forms.CharField):
 
    def clean(self, value):
        #forms.Field.clean(self, value)
        value = super(ColorField, self).clean(value)
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
        #forms.Field.clean(self, value)
        value = super(HourField, self).clean(value)
        #self.max_length=4
        try:
            value = int(value)
        except ValueError: 
            raise forms.ValidationError(_('Must be a number'))
        #raise AssertionError(value)
        if value < -1000  or 1000 < value:
            raise forms.ValidationError(_('Number out of range.'))

        return value

class TypeDropField(forms.CharField):
    
    def __init__(self, *args, **kwargs):
        super(TypeDropField, self).__init__(*args,**kwargs)
    
    def clean(self, value):
        value = super(TypeDropField, self).clean(value)
        p = re.compile('^[a-zA-Z0-9_ ,]*$')
        if not p.match(value):
            raise forms.ValidationError(_('Must be a comma separated word list of only letters, numbers or underscores.'))
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
        if int(EventType.objects.filter(type_name__iexact=type_name_input, type_active=True, org_name=self._current_org).exclude(id=self.instance.id).count() >= 1):
            raise forms.ValidationError(_("Type Name already exists."))
        return type_name_input


class EventForm(forms.ModelForm):
    event_desc = forms.CharField(widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
    event_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'id':'id_event_date',},format="%m/%d/%Y %H:%M"))
    event_signup_deadline = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'id':'id_event_signup_deadline',},format="%m/%d/%Y %H:%M"))    
    
    def __init__(self, current_org, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["event_type"].queryset = EventType.objects.filter(org_name=current_org, type_active=True)
        
        self.fields['att_type_col1'].widget.attrs = {'id':'id_att_type_col1'}
        self.fields['att_type_col2'].widget.attrs = {'id':'id_att_type_col2'}
        self.fields['att_type_col3'].widget.attrs = {'id':'id_att_type_col3'} 
        self.fields['att_type_col4'].widget.attrs = {'id':'id_att_type_col4'} 
        self.fields['att_type_col5'].widget.attrs = {'id':'id_att_type_col5'} 
        self.fields['att_type_col6'].widget.attrs = {'id':'id_att_type_col6'}    
        # retain the characteristics of a CharField, but add TypeDropField validation 
        # http://wadofstuff.blogspot.com/2009/02/django-dry-custom-model-forms-and.html
        field = self.Meta.model._meta.get_field('att_type_drop_col1')
        self.fields['att_type_drop_col1'] = field.formfield(form_class=TypeDropField)
        self.fields['att_type_drop_col1'].widget.attrs = {'id':'id_att_type_drop_col1'} 
        field = self.Meta.model._meta.get_field('att_type_drop_col2')
        self.fields['att_type_drop_col2'] = field.formfield(form_class=TypeDropField)                        
        self.fields['att_type_drop_col2'].widget.attrs = {'id':'id_att_type_drop_col2'} 
        field = self.Meta.model._meta.get_field('att_type_drop_col3')
        self.fields['att_type_drop_col3'] = field.formfield(form_class=TypeDropField)          
        self.fields['att_type_drop_col3'].widget.attrs = {'id':'id_att_type_drop_col3'}
        field = self.Meta.model._meta.get_field('att_type_drop_col4')
        self.fields['att_type_drop_col4'] = field.formfield(form_class=TypeDropField)   
        self.fields['att_type_drop_col4'].widget.attrs = {'id':'id_att_type_drop_col4'} 
        field = self.Meta.model._meta.get_field('att_type_drop_col5')
        self.fields['att_type_drop_col5'] = field.formfield(form_class=TypeDropField)  
        self.fields['att_type_drop_col5'].widget.attrs = {'id':'id_att_type_drop_col5'} 
        field = self.Meta.model._meta.get_field('att_type_drop_col6')
        self.fields['att_type_drop_col6'] = field.formfield(form_class=TypeDropField)  
        self.fields['att_type_drop_col6'].widget.attrs = {'id':'id_att_type_drop_col6'} 
        
    class Meta:
        
        js = (
            settings.STATIC_URL + "js/SelectBox.js",
            settings.STATIC_URL + "js/SelectFilter2.js",
            settings.STATIC_URL + 'js/jqui/js/jquery-1.3.2.min.js',
            settings.STATIC_URL + 'js/ajax_filtered_fields/ajax_filtered_fields.js',
        )
        
        model = Event
        exclude = ('event_org','event_hash','event_creator_name','event_created_date','event_active',)
   
    
class AttendeeForm(forms.ModelForm):

    def parse_csv(self, csv):
        l =   [("","")] +  [ (i, i) for i in csv.split(',') ]
        return l

    def __init__(self, current_event, *args, **kwargs):
        super(AttendeeForm, self).__init__(*args, **kwargs)
        if current_event.event_track_hours:
            self.fields['att_hours'] =  HourField(widget=forms.TextInput(attrs={'size':'5',}), max_length=5)
            
        for index in range(1, 6):
            attr_col = 'att_col%s' % (index)
            att_header_col = 'att_header_col%s' % (index)
            att_require_col = 'att_require_col%s' % (index)
            att_type_col = 'att_type_col%s' % (index)
            att_type_drop_col = 'att_type_drop_col%s' % (index)
            if getattr(current_event, att_header_col):
                if getattr(current_event, att_type_col) == 1:
                    self.fields[attr_col] = forms.BooleanField(
                                                widget=forms.CheckboxInput(), 
                                                label=getattr(current_event, att_header_col) , 
                                                required=getattr(current_event, att_require_col ) 
                                                )
                elif getattr(current_event, att_type_col) == 2:
                    self.fields[attr_col] = forms.CharField(
                                                widget=forms.Select(choices = self.parse_csv(getattr(current_event, att_type_drop_col ))), 
                                                label=getattr(current_event, att_header_col) , 
                                                required=getattr(current_event, att_require_col )
                                                )
                elif getattr(current_event, att_type_col) == 3:
                    self.fields[attr_col] = forms.IntegerField(
                                                widget=forms.TextInput(attrs = {'size':'15',}), 
                                                label=getattr(current_event, att_header_col), 
                                                required=getattr(current_event, att_require_col )
                                                )
                else:
                    self.fields[attr_col] = forms.CharField(
                                                widget=forms.TextInput(attrs = {'size':'30',}), 
                                                label=getattr(current_event, att_header_col),
                                                required=getattr(current_event, att_require_col )
                                                )
    class Meta:
        model = Attendee
        exclude = ('att_ip','att_event','att_name','att_hours','att_col1','att_col2','att_col3','att_col4','att_col5','att_col6')
        
