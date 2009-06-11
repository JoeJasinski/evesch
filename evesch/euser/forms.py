from django import forms 
from django.forms import ModelForm

from euser.models import User 

class UserForm(ModelForm):
    about = forms.CharField(
         widget=forms.TextInput(attrs = {'cols': '30', 'rows': '5'}))
    class Meta:
        model = User
        #exclude = ('',)
        
