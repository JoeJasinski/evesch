from django import forms 
from django.forms import ModelForm

from euser.models import eUser 

class UserForm(ModelForm):
    about = forms.CharField(required=False, widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))
    class Meta:
        model = eUser
        fields = ('first_name','last_name','gender','city','country','email','phone','about',)
        #exclude = ('',)
        
