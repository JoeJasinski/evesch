from django.db import models
from org.models import Organization
from euser.models import eUser
from event.models import Event
from datetime import datetime

class Post(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(eUser)
    org = models.ForeignKey(Organization)
    event = models.ForeignKey(Event, blank=True, null=True)
    date = models.DateTimeField()

    def save(self):
        if not self.id:
            self.date = datetime.now()
        super(Post, self).save()
    
    def __unicode__(self):
        return "Post in %s" %  (self.org)