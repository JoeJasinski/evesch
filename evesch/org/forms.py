from django import forms
from django.forms import ModelForm, Form
from org.models import Organization
from django.utils.translation import ugettext_lazy as _

class OrganizationForm(ModelForm):
    org_short_name = forms.CharField()
    org_desc = forms.CharField(max_length=512,
         widget=forms.Textarea(attrs = {'cols': '45', 'rows': '5'}))
    class Meta:
        model = Organization
        exclude = ('org_date_created','org_feed_hash',)
        
    def clean_org_short_name(self):
        org_short_name=self.cleaned_data['org_short_name']
        num_chars = len(org_short_name)
        if num_chars < 3:
            raise forms.ValidationError(_("Org Short Name must be 3 characters or more."))
        else:
            if int(Organization.objects.filter(org_short_name=org_short_name).count()) >= 1:
                raise forms.ValidationError(u"Org Short Name already exists.")
        return org_short_name
    

class OrganizationJoinForm(Form):
    ''' Here for future use - if the Org admin wants to have a user fill out a form before joining '''
    pass

class OrganizationFormEdit(ModelForm):
    org_desc = forms.CharField(max_length=512,
         widget=forms.Textarea(attrs = {'cols': '45', 'rows': '5'}))
    class Meta:
        model = Organization
        exclude = ('org_date_created','org_short_name','org_feed_hash',)
        

class OrganizationInviteMember(Form):
    invite_list = forms.CharField(max_length=512,
         widget=forms.Textarea(attrs = {'cols': '45', 'rows': '5','id':'invite_member_form'}))



        
