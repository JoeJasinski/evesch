from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.conf import settings

def avatar_img(avatar, size):
    if not avatar.thumbnail_exists(size):
        avatar.create_thumbnail(size)
    return mark_safe("""<img src="%s" alt="%s" width="%s" height="%s" />""" % 
        (avatar.avatar_url(size), unicode(avatar), size, ((size * 3) / 4)))

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

class UploadAvatarForm(forms.Form):
    avatar = forms.ImageField(required=False, label="Upload a photo")

    def clean_avatar(self):

        if self.cleaned_data.get('avatar'):
            photo_data = self.cleaned_data['avatar']
            if 'error' in photo_data:
                raise forms.ValidationError(_('Upload a valid image. The file you uploaded was either not an image or a corrupted image.'))

        content_type = photo_data.content_type
        if content_type:
            main, sub = content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'gif', 'png']):
                raise forms.ValidationError(_('JPEG, PNG, GIF only.'))
            
        size = photo_data.size
        if size > settings.MAX_PHOTO_UPLOAD_SIZE * 1024:
            raise forms.ValidationError(_('Image too big ' + str(size)))
        #raise forms.ValidationError(dir(photo_data))
        #width, height = photo_data['dimensions']
        #if width > settings.MAX_PHOTO_WIDTH:
        #    raise forms.ValidationError(_('Max width is %s' % settings.MAX_PHOTO_WIDTH))
        #if height > settings.MAX_PHOTO_HEIGHT:
        #    raise forms.ValidationError(_('Max height is %s' % settings.MAX_PHOTO_HEIGHT))       
           
        return self.cleaned_data['avatar']
