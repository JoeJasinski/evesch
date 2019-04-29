from datetime import datetime
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from random import sample
from evesch.core.lib import Message
from evesch.core.middleware import threadlocals 
from django.conf import settings

KEYS = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class OrganizationManager(models.Manager):

    def create_organization(self, org_name, org_short_name):
        organization = Organization(org_name=org_name, org_short_name=org_short_name)

        organization.org_date_created = datetime.now()
        organization.save()
        #user_group = UserGroup.objects.create_user_group()
        return organization 

    def get_current_org(self, org_short_name, message=None):
        if message:
            return None, message
        else:
            try:
                current_org = super(OrganizationManager, self).get(
                    org_short_name=org_short_name, org_active=True)
            except:
                current_org =  None
                message = Message(
                    title="Org Not Found",
                    text="The organization was not found")
        return current_org, message

    def get_browsable_orgs(self):
        return super(OrganizationManager, self).filter(
            org_browsable=True, org_active=True).order_by("org_name")


class Organization(models.Model):

    ORG_TYPES = (
        (0, 'None'),
        (1, 'Non Profit'),
        (2, 'Business'),
        (3, 'Community'),
        (4, 'Social'),
        (5, 'School'),
    )

    ORG_JOIN_PRIVACY = (
        (0, 'Public'),
        (1, 'Invite Only'),
        (2, 'Request Membership'),
    )

    org_name = models.CharField(
        verbose_name="Organization Name",
        db_index=True,
        max_length=64)
    org_short_name = models.SlugField(
        verbose_name=_("Organization Short Name"),
        max_length=20,
        db_index=True)
    org_active = models.BooleanField(
        verbose_name=_("Organization Active"),
        help_text=_("Does the Organization exist?"),
        default=True)
    org_desc = models.CharField(
        verbose_name=_("Organization Description"),
        default="",
        max_length=512, 
        blank=True, null=True)
    org_email = models.EmailField(
        verbose_name=_("Organization Email"),
        blank=True, null=True)
    org_website = models.URLField(
        verbose_name=_("Organization Website"),
        blank=True, null=True)
    org_phone = models.CharField(
        max_length=50,
        verbose_name=_("Organization Phone Number"),
        blank=True, null=True)
    org_address = models.CharField(
        max_length=100,
        blank=True, null=True)
    org_city = models.CharField(
        max_length=80,
        verbose_name=_("Organization City"),
        blank=True, null=True)
    org_state = models.CharField(
        max_length=32,
        verbose_name=_("Organization State"),
        blank=True, null=True)
    org_zip = models.CharField(
        max_length=10,
        verbose_name=_("Organization Zip Code"),
        blank=True, null=True,)
    org_type = models.IntegerField(
        choices=ORG_TYPES,
        blank=True, null=True, default=0)
    org_date_created = models.DateTimeField(
        null=True, auto_now_add=True)
    org_feed_hash =  models.CharField(
        max_length=20,
        verbose_name=_("Organization Feed Hash"),
        null=True, blank=True)
    org_join_privacy = models.IntegerField(
        choices=ORG_JOIN_PRIVACY,
        default=0,
        verbose_name=_("Organization Join Privacy"),
        help_text=_("<u>Public:</u> any user may join this organization. "
                    "<BR><u>Invite Only:</u> a user must receive an "
                    "invitation from someone in the org.  <BR><u>Request Membership:</u> "
                    "a user must request membership to join that must be "
                    "confirmed by someone in the org."),
        null=True, blank=True,)
    org_browsable = models.BooleanField(
        default=True,
        verbose_name=_("Browsable"),
        help_text=_("List this organization in the public Browse directory? "
                    "(recommended) Authenticated users will still be able to see it."))

    objects = OrganizationManager()

    def __str__(self):
        return "{}".format(self.org_name)

    def get_events(self):
        return self.event_set.filter(event_active=True)

    def get_eventtypes(self):
        return self.eventtype_set.filter(type_active=True)

    def get_org_groups(self):
        return self.group_set.all()

    def get_org_admin_groups(self):
        return self.group_set.filter(admin_org=True)

    def get_coordinator_groups(self):
        return self.group_set.filter(coord_events=True)

    def get_orginvite_groups(self):
        return self.group_set.filter(invite_users=True)

    def get_members(self):
        return self.org_users.all()

    def get_member_count(self):
        return self.org_users.all().count()

    def get_admin_users(self):
        return get_user_model().objects.filter(
            user_groups__in=self.get_org_admin_groups())
        #return self.get_members().filter(user_groups__in=self.get_org_admin_groups())
        # not sure if the commented syntax works.  Check

    # TODO: UNTESTED - was on the train and had to go before testing
    def get_invited_users(self):	
        return get_user_model().objects.filter(
            user_invites_set__in=self.invite_set.all())

    def get_coordinator_users(self):
        return get_user_model().objects.filter(
            user_groups__in=self.get_coordinator_groups())

    def get_orginvite_users(self):
        """Get users who can invite people to the org"""
        return get_user_model().objects.filter(
            user_groups__in=self.get_orginvite_groups())

    def get_current_event(self, event_hash, message=None):
        if message:
            return None, message
        else:
            try:
                return self.event_set.get(
                    event_active=True, event_hash=event_hash), message
            except:
                current_event = None
                message = Message(
                    title="Event Not Found",
                    text="The event was not found")
            return current_event, message

    def get_absolute_url(self):
        return reverse('org_org_view', kwargs={'org_short_name': self.org_short_name,})

    def is_member(self, user):
        if self.org_users.filter(id=user.id):
            return True
        else:
            return False	

    def org_perms(self, user):
        permissions = {
            'can_add_event': False,   #  user can create event in current org
            'can_remove_org': False,  #  user can remove the current org
            'can_join_org': False,    #  user can join the current org
            'can_edit_org': False,    #  user can edit the current org
            'is_memberof_org': False, #  user is a member of current org
            'can_add_type': False,    #  user can add event type to current org
            'can_remove_type': False, #  user can remove event type from current org
            'can_edit_type': False,   #  user can edit event_type in current_rog
            'can_edit_group': False,  #  user can edit the groups in the org
            'can_remove_groupmember': False, #  user can remove a member of the group
            'can_add_group': False,   #  user can add groups to this org
            'can_remove_group': False, #  user can remove groups in this org
            'can_remove_users': False, #  user can remove users in theis org
            'can_invite_users': False, #  user can invite users to theis org
        }

        permissions['is_memberof_org'] = self.is_member(user)
        if user.is_superuser == 1:
            permissions['can_join_org'] = True
            if permissions['is_memberof_org']:
                permissions['can_add_event'] = True
                permissions['can_remove_org'] = True
                permissions['can_edit_org'] = True
                permissions['can_add_type'] = True
                permissions['can_remove_type'] = True
                permissions['can_edit_type'] = True
                permissions['can_edit_group'] = True
                permissions['can_remove_groupmember'] = True
                permissions['can_add_group'] = True
                permissions['can_remove_group'] = True
                permissions['can_remove_users'] = True
                permissions['can_invite_users'] = True
        elif self.get_admin_users().filter(id=user.id):
            permissions['can_join_org'] = True
            if permissions['is_memberof_org']:
                permissions['can_add_event'] = True
                permissions['can_remove_org'] = True
                permissions['can_edit_org'] = True
                permissions['can_add_type'] = True
                permissions['can_remove_type'] = True
                permissions['can_edit_type'] = True
                permissions['can_edit_group'] = True
                permissions['can_remove_groupmember'] = True
                permissions['can_add_group'] = True
                permissions['can_remove_group'] = True
                permissions['can_remove_users'] = True
                permissions['can_invite_users'] = True			
        elif self.get_coordinator_users():
            permissions['can_join_org'] = True
            if permissions['is_memberof_org']:
                permissions['can_add_event'] = True
        else:
            if self.org_join_privacy == 0:
                permissions['can_join_org'] = True	
            if self.org_join_privacy == 1 or self.org_join_privacy == 2:
                from org.models import OrgInvite
                if  OrgInvite.objects.filter(org=self, user=user, direction=True) > 0:
                    permissions['can_join_org'] = True

        if permissions['is_memberof_org']:
            if self.get_orginvite_users().filter(id=user.id):
                permissions['can_invite_users'] = True

        return permissions

    def save(self, *args, **kwargs):
        if len(str(self.org_feed_hash)) != 20:
            self.org_feed_hash = "".join(sample(KEYS, 20))
        if not self.org_date_created:
            self.org_date_created = datetime.now()
        super(Organization, self).save(*args, **kwargs)


class OrgInvite(models.Model):
    org = models.ForeignKey(
        Organization,
        related_name="invite_set",
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        related_name="user_invites_set",
        on_delete=models.CASCADE)
    email = models.EmailField(
        _('Anonymous email'),
        blank=True, null=True)
    direction = models.BooleanField(
        default=True)
    invite_hash = models.CharField(
        db_index=True,					
        max_length=20,
        verbose_name=_("Invite Hash"),
        null=True, blank=True,)

    def save(self, *args, **kwargs):
        if len(str(self.invite_hash)) != 20:
            self.invite_hash = "".join(sample(KEYS, 20))
        super(OrgInvite, self).save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return "{} invited to {}".format(self.user, self.org)
        else:
            return "{} invited to {}".format(self.email, self.org)
