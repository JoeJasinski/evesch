from django import forms 
from django.forms import ModelForm

from egroup.models import UserGroup

class UserGroupForm(ModelForm):
    group_desc = forms.CharField(
         widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
    class Meta:
        model = UserGroup
        exclude = ['org_name','group_removable','group_hash',]
        
        
class UserGroupEditForm(ModelForm):
    group_desc = forms.CharField(
         widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
    class Meta:
        model = UserGroup
        exclude = ['org_name','group_hash','group_removable',]
