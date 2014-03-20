from datetime import datetime
from django.db import models
from evesch.org.models import Organization
from evesch.event.models import Event
from django.conf import settings

class Post(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    org = models.ForeignKey(Organization)
    event = models.ForeignKey(Event, blank=True, null=True)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = datetime.now()
        super(Post, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "Post in %s" %  (self.org)