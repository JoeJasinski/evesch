from django import forms
from django.utils.translation import ugettext_lazy as _
import re
from euser.models import User

class CaptchaField(forms.CharField):
 
    def clean(self, value):
        if not value:
            raise forms.ValidationError(_('You must enter a valid Captcha value'))
            
        p = re.compile('^[a-zA-Z]+$')
        if not p.match(value):
            raise forms.ValidationError(_('Only letters acceptable'))
                      
        return value


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
    captcha = CaptchaField()
    session_captcha = None

    def __init__(self, session_captcha, *args, **kwargs):
        self.session_captcha = session_captcha
        super(SignupForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        post_email = self.cleaned_data['email']
        if User.objects.filter(email=post_email):
            raise forms.ValidationError(_("This email is already registered."))
        return post_email

    def clean_username(self):
        post_username = self.cleaned_data['username']
        p = re.compile('^\w+$')
        if not p.match(post_username):
            raise forms.ValidationError(_("You must use only letters, numbers, or an underscore"))
        if User.objects.filter(username=post_username):
           raise forms.ValidationError(_("User already exists."))  
        return post_username
    
    def clean_captcha(self):
        post_captcha = self.cleaned_data['captcha']
        if self.session_captcha:
            if post_captcha != self.session_captcha:
                raise forms.ValidationError(_("You must correctly enter the text in the box."))    
        return post_captcha

    def clean(self):
        cleaned_data = self.cleaned_data
        posted_password = cleaned_data.get("password")
        posted_password_verify = cleaned_data.get("password_verify")
        if posted_password != posted_password_verify:
            raise forms.ValidationError(_("Passwords to not match."))    
        return cleaned_data

class SignupConfirmForm(forms.Form):
    security_hash = forms.CharField(max_length=24)
    
class PasswordResetForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    captcha = CaptchaField()
    session_captcha = None   
    
    def __init__(self, session_captcha, *args, **kwargs):
        self.session_captcha = session_captcha
        super(PasswordResetForm, self).__init__(*args, **kwargs)
    
    def clean_captcha(self):
        post_captcha = self.cleaned_data['captcha']
        #raise AssertionError(self.session_captcha)
        if self.session_captcha:
            if post_captcha != self.session_captcha:
                raise forms.ValidationError(_("You must correctly enter the text in the box."))
        return post_captcha
    
    def clean(self):
        cleaned_data = self.cleaned_data
        post_username = cleaned_data.get("username")
        post_email = cleaned_data.get("email")
        if post_username or post_email:
            if post_username:
                if not User.objects.filter(username=post_username):
                    raise forms.ValidationError(_("No such user."))  
            else:
                if not User.objects.filter(email=post_email):
                    raise forms.ValidationError(_("This email is not registered."))
        else:
            raise forms.ValidationError(_("Must supply a username or email address"))
        
        return cleaned_data