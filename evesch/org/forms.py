from django import forms
from django.forms import ModelForm, Form
from django.utils.translation import ugettext_lazy as _
from evesch.org.models import Organization


class OrganizationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.fields['org_desc'].widget=forms.Textarea(
            attrs={'cols': '45', 'rows': '5'}) 
    
    class Meta:
        model = Organization
        exclude = (
            'org_date_created',
            'org_feed_hash',
            'org_active', )
        
    def clean_org_short_name(self):
        org_short_name=self.cleaned_data['org_short_name']
        num_chars = len(org_short_name)
        if num_chars < 3:
            raise forms.ValidationError(_("Org Short Name must be 3 characters or more."))
        else:
            if int(Organization.objects.filter(org_short_name=org_short_name).count()) >= 1:
                raise forms.ValidationError(_("Org Short Name already exists."))
        return org_short_name
    

class OrganizationJoinForm(Form):
    """Here for future use - if the Org admin wants to have a user fill 
    out a form before joining
    """


class OrganizationFormEdit(ModelForm):
    class Meta:
        model = Organization
        exclude = (
            'org_date_created',
            'org_short_name',
            'org_feed_hash',
            'org_active', )

    def __init__(self, *args, **kwargs):
        super(OrganizationFormEdit, self).__init__(*args, **kwargs)
        self.fields['org_desc'].widget = forms.Textarea(
            attrs={'cols': '45', 'rows': '5'})        


class OrganizationInviteMember(Form):
    invite_list = forms.CharField(
        required=False,
        max_length=512,
        widget=forms.Textarea(
            attrs={'cols': '45', 'rows': '5', 'id':'invite_member_form'}))
    
    def clean_invite_list(self):
        user_string = self.cleaned_data['invite_list']
        user_string = user_string.strip().strip(',').strip()
        return user_string

    class Meta:
        exclude = ('direction', )
