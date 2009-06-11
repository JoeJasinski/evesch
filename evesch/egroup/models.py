from django.utils.translation import ugettext_lazy as _
from django.db import models
from org.models import Organization
from random import sample
from core.lib import Message

KEYS='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class UserGroupManager(models.Manager):
    def create_user_group(self,group_name,org_name,group_desc=None):
        user_group = UserGroup(group_name=group_name, 
                               org_name=org_name)
        user_group.group_desc = group_desc
        user_group.save()
        return user_group
        
    def init_org_groups(self,org,user):
            admin_group = UserGroup(group_name= "%s - Admin Group" % (org.org_name,),
                                    group_hash= "%s_adm" % (org.org_short_name,),
                                    group_desc=_("Administrator Group"), group_removable=False, 
                                    admin_org=True, coord_events=True, org_name=org)
            admin_group.save()
            event_coordinator_group = UserGroup(group_name="%s - Event Coordinator Group" % (org.org_name,),
                                    group_hash="%s_crd" % (org.org_short_name,),
                                    group_desc=_("Event Coordinator Group"), group_removable=False,
                                    admin_org=False, coord_events=True, org_name=org)
            event_coordinator_group.save()
            user.user_groups.add(admin_group)
            user.user_groups.add(event_coordinator_group)
            user.user_organizations.add(org)

    def get_current_usergroup(self,group_hash, message=None):
        if message:
            return None, message
        else:
            try:
                current_usergroup = super(UserGroupManager, self).get(group_hash=group_hash)
            except:
                current_usergroup = None
                message = Message(title=_("User Group Not Found"), text=_("The user group was not found"))
            return current_usergroup, message

class UserGroup(models.Model):
    
    group_name = models.CharField(
        max_length=96,)
    group_hash = models.SlugField(
        max_length=16)
    group_desc = models.TextField(blank=True,null=True)
    group_removable = models.BooleanField(default=False)
    admin_org = models.BooleanField(default=False,)
    coord_events = models.BooleanField(default=False,)
    org_name = models.ForeignKey(Organization, related_name='group_set')
    objects = UserGroupManager()

    def __unicode__(self):
        return "%s - %s" % (self.group_name, self.group_hash)
    
    def __int__(self):
        return self.pk
    
    def save(self):
        if not self.id:
            self.group_hash = "".join(sample(KEYS,16))
        
        super(UserGroup, self).save()