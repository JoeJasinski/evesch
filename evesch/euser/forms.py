from django import forms 
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from evesch.euser.models import eUser 

class UserForm(ModelForm):
    about = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs = {'cols': '30', 'rows': '5'}))

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'gender',
            'city',
            'country',
            'email',
            'phone',
            'about',)
        #exclude = ('',)        
