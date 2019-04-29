from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.exceptions import ObjectDoesNotExist


class ReportFilterForm(forms.Form):
    min_event_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'id': _('min_event_date_input'), 'size': "12",}))
    max_event_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'id': _('max_event_date_input'), 'size': "12",}))
