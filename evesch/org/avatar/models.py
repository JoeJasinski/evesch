import datetime
import os.path

from django.db import models
from django.core.files.base import ContentFile
from django.utils.translation import ugettext as _
from evesch.org.models import Organization
from django.conf import settings

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from PIL import Image
except ImportError:
    import Image

def upload_file_path(instance, filename):
    path =  os.path.abspath(os.path.join(settings.MEDIA_ROOT, instance.org.org_short_name, filename))
    return path

class Avatar(models.Model):
    org = models.ForeignKey('org.Organization')
    primary = models.BooleanField(default=False)
    avatar = models.ImageField(max_length=1024, upload_to=upload_file_path, blank=True)
    date_uploaded = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return _(u'Photo for %s') % self.org.org_short_name
    
    def save(self, *args, **kwargs):
        super(Avatar, self).save(*args, **kwargs)
        if self.primary:
            Avatar.objects.filter(org=self.org, primary=True).exclude(id=self.id).update(primary=False)