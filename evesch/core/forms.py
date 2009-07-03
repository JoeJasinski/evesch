from django import forms
from django.utils.translation import ugettext_lazy as _


class MessageForm(forms.Form):
    subject = forms.CharField(max_length=50)
    body = forms.CharField(widget=forms.Textarea(attrs = {'cols': '45', 'rows': '5'}), max_length=512)
    
class EveschLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    
class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password_verify = forms.CharField(widget=forms.PasswordInput(render_value=False))
    email = forms.EmailField()
    captcha = forms.CharField()

    def clean(self):
        cleaned_data = self.cleaned_data
        posted_username = cleaned_data.get("username")
        posted_password = cleaned_data.get("password")
        posted_password_verify = cleaned_data.get("password_verify")
    
        if posted_password != posted_password_verify:
            raise forms.ValidationError(_("Passwords to not match."))

        from euser.models import User
        if User.objects.filter(username=posted_username):
           raise forms.ValidationError(_("User already exists."))    
        
        return cleaned_data

    
class PasswordResetForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()