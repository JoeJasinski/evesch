from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

def avatar_img(avatar, size):
    if not avatar.thumbnail_exists(size):
        avatar.create_thumbnail(size)
    return mark_safe("""<img src="%s" alt="%s" width="%s" height="%s" />""" % 
        (avatar.avatar_url(size), unicode(avatar), size, size))

class PrimaryAvatarForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org')
        size = kwargs.pop('size', 80)
        super(PrimaryAvatarForm, self).__init__(*args, **kwargs)
        avatars = org.avatar_set.all()
        self.fields['choice'] = forms.ChoiceField(label=_("Available Photos"),
            choices=[(c.id, avatar_img(c, size)) for c in org.avatar_set.all()],
            widget=widgets.RadioSelect)

class DeleteAvatarForm(forms.Form):

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org')
        size = kwargs.pop('size', 80)
        super(DeleteAvatarForm, self).__init__(*args, **kwargs)
        avatars = org.avatar_set.all()
        self.fields['choices'] = forms.MultipleChoiceField(label=_("Available Photos"),
            choices=[(c.id, avatar_img(c, size)) for c in org.avatar_set.all()],
            widget=widgets.CheckboxSelectMultiple)
