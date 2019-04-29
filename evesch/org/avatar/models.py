import datetime
import os.path
from io import StringIO
from PIL import Image
from django.db import models
from django.core.files.base import ContentFile
from django.utils.translation import ugettext as _
from evesch.org.models import Organization

from evesch.org.avatar import AVATAR_STORAGE_DIR, AVATAR_RESIZE_METHOD

def avatar_file_path(instance=None, filename=None, org_short_name=None):
    return os.path.join(AVATAR_STORAGE_DIR, org_short_name, filename)


class Avatar(models.Model):
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE)
    primary = models.BooleanField(
        default=False)
    avatar = models.ImageField(
        max_length=1024,
        upload_to=avatar_file_path,
        blank=True)
    date_uploaded = models.DateTimeField(
        default=datetime.datetime.now)

    def __str__(self):
        return _('Avatar for {}'.format(self.org.org_short_name))

    def save(self, force_insert=False, force_update=False):
        if self.primary:
            avatars = Avatar.objects.filter(org=self.org, primary=True).exclude(id=self.id)
            avatars.update(primary=False)
        super(Avatar, self).save(force_insert, force_update)

    def thumbnail_exists(self, size):
        return self.avatar.storage.exists(self.avatar_name(size))

    def create_thumbnail(self, size):
        try:
            orig = self.avatar.storage.open(self.avatar.name, 'rb').read()
            image = Image.open(StringIO(orig))
        except IOError:
            return # What should we do here?  Render a "sorry, didn't work" img?
        (w, h) = image.size

        width = size
        if w != width or h != ((width * 3) / 4):
            #if taller than ratio...
            if h / w > 0.75:
                h1 = ((w * 3) / 4)
                image = image.crop((0, (h / 2) - (h1 / 2), w, (h / 2) + (h1 / 2)))
            else:
                w1 = ((h * 4) / 3)
                image = image.crop(((w / 2 ) - (w1 / 2), 0, (w / 2) + (w1 / 2), h))
            image = image.resize((width, ((width * 3) / 4)), AVATAR_RESIZE_METHOD)
        
            if image.mode != "RGB":
                image = image.convert("RGB")
            thumb = StringIO()
            image.save(thumb, "JPEG")
            thumb_file = ContentFile(thumb.getvalue())
        else:
            thumb_file = ContentFile(orig)
        thumb = self.avatar.storage.save(self.avatar_name(size), thumb_file)

    def avatar_url(self, size):
        return self.avatar.storage.url(self.avatar_name(size))

    def avatar_name(self, size):
        return os.path.join(
            AVATAR_STORAGE_DIR, self.org.org_short_name,
            'resized', str(size), self.avatar.name)
