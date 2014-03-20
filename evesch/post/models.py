from datetime import datetime
from django.db import models
from evesch.org.models import Organization
from evesch.euser.models import eUser
from evesch.event.models import Event

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