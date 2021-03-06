from random import sample
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db import models
from django.core.urlresolvers import reverse
from evesch.org.models import Organization
from evesch.core.lib import Message

KEYS='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class UserGroupManager(models.Manager):
    def create_user_group(self,group_name,org_name,group_desc=None):
        user_group = UserGroup(group_name=group_name, 
                               org_name=org_name)
        user_group.group_desc = group_desc
        user_group.save()
        return user_group
        
    def init_org_groups(self,org,user):
        admin_desc_text = ugettext("People in this group can administer the organization.")
        admin_group = UserGroup(group_name= "Administrator Group",
                                group_desc=admin_desc_text, group_removable=False, 
                                admin_org=True, coord_events=True, invite_users=True, org_name=org)
        admin_group.save()
        coord_desc_text = ugettext("People in this group can create and organize events.")
        event_coordinator_group = UserGroup(group_name="Event Coordinator Group",
                                group_desc=coord_desc_text, group_removable=False,
                                admin_org=False, coord_events=True, invite_users=True, org_name=org)
        coord_desc_text = ugettext("Everyone in the organization is in this group.")
        event_coordinator_group.save()
        everyone_group = UserGroup(group_name="Everyone Group",
                                group_desc=coord_desc_text, group_removable=False,
                                admin_org=False, coord_events=False, invite_users=False, meta=1, org_name=org)        
        everyone_group.save()
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
    
    GROUP_META = (
        (0,'None'),
        (1,'Everyone'),
    )

    group_name = models.CharField(
        max_length=40,)
    group_hash = models.SlugField(
        max_length=16)
    group_desc = models.TextField(blank=True,null=True)
    group_removable = models.BooleanField(default=False)
    admin_org = models.BooleanField(default=False,)
    coord_events = models.BooleanField(default=False,)
    invite_users = models.BooleanField(default=False,)
    meta = models.IntegerField(default=0, choices=GROUP_META)
    org_name = models.ForeignKey(Organization, related_name='group_set')
    objects = UserGroupManager()

    def __unicode__(self):
        return "%s - %s - %s" % (self.org_name.org_short_name, self.group_name, self.group_hash)
    
    def __int__(self):
        return self.pk
    
    def get_members(self):
        if self.meta == 1:
            return self.org_name.get_members()
        else:
            return self.group_users.all()

    def get_absolute_url(self):
        return reverse('egroup_group_view',kwargs={'org_short_name':self.org_name.org_short_name,'group_hash':self.group_hash,})
    
    def save(self):
        if not self.id:
            self.group_hash = "".join(sample(KEYS,16))
        super(UserGroup, self).save()