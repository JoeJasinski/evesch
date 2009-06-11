from django import forms

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
    
class PasswordResetForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()