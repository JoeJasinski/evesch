from django import forms 
from egroup.models import UserGroup

class UserGroupForm(forms.ModelForm):
    group_desc = forms.CharField(
         widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
    class Meta:
        model = UserGroup
        exclude = ['org_name','group_removable','group_hash',]
            
class UserGroupEditForm(forms.ModelForm):
    group_desc = forms.CharField(widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
    action = forms.CharField(widget=forms.HiddenInput(attrs={'value':'group_edit'}))
    class Meta:
        model = UserGroup
        exclude = ['org_name','group_hash','group_removable',]

class GroupAddMemberForm(forms.Form):
    user_list = forms.CharField(required=False, max_length=512,
         widget=forms.Textarea(attrs = {'cols': '45', 'rows': '5','id':'add_user_form'}))
    action = forms.CharField(widget=forms.HiddenInput(attrs={'value':'group_member_add'}))
    def clean_user_list(self):
        user_string = self.cleaned_data['user_list']
        user_string = user_string.strip().strip(',').strip()
        return user_string

