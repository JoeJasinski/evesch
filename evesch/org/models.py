from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from random import sample
from core.lib import Message
from euser.models import User
from django.core.urlresolvers import reverse

KEYS='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

class OrganizationManager(models.Manager):

	def create_organization(self, org_name, org_short_name ):
		organization = Organization(org_name=org_name,org_short_name=org_short_name, )

		organization.org_date_created = datetime.now()
		organization.save()
		#user_group = UserGroup.objects.create_user_group()
		return organization 

	def get_current_org(self,org_short_name, message=None):
		if message:
			return None, message
		else:
			try:
				current_org = super(OrganizationManager, self).get(org_short_name=org_short_name, org_active=True)
			except:
				current_org =  None
				message = Message(title="Org Not Found", text="The organization was not found")
		return current_org, message

class Organization(models.Model):

	ORG_TYPES = (
		(0,'None'),
		(1,'Non Profit'),
		(2,'Business'),
		(3,'Community'),
		(4,'Social'),
		(5,'School'),
	)

	ORG_JOIN_PRIVACY = (
		(0,'Public'),
		(1,'Invite Only'),
		(2,'Request Membership'),
	)

	org_name = models.CharField(
		db_column = "org_name",
		verbose_name="Organization Name",
		db_index = True,
		max_length=64)
	org_short_name = models.SlugField(
		db_column="org_short_name",
		verbose_name=_("Organization Short Name"),
		max_length=20,
		db_index=True)
	org_active = models.BooleanField(
		db_column = "org_active",
		verbose_name = _("Organization Active"),
		help_text = _("Does the Organization exist?"),
		default = True)
	org_desc = models.CharField(
		db_column = "org_desc",
		verbose_name=_("Organization Description"),
		max_length=512, 
		blank=True, null=True)
	org_email = models.EmailField(
		db_column = "org_email",
		verbose_name=_("Organization Email"),
		blank=True, null=True)
	org_website = models.URLField(
		db_column = "org_website",
		verbose_name=_("Organization Website"),
		verify_exists = False,
		blank=True, null=True)
	org_phone = models.CharField(
		db_column = "org_phone",
		max_length=50,
		verbose_name=_("Organization Phone Number"),
		blank=True, null=True)
	org_address = models.CharField(
		db_column = "org_address",
		max_length=100,
		blank=True, null=True)
	org_city = models.CharField(
		db_column = "org_city",
		max_length="80",
		verbose_name=_("Organization City"),
		blank=True, null=True)
	org_state = models.CharField(
		db_column = "org_state",
		max_length="32",
		verbose_name=_("Organization State"),
		blank=True, null=True)
	org_zip = models.CharField(
		db_column = "org_zip",
		max_length="10",
		verbose_name=_("Organization Zip Code"),
		blank=True, null=True,)
	org_type = models.IntegerField(
		db_column = "org_type",
		choices = ORG_TYPES,
		blank=True, null=True, default=0)
	org_date_created = models.DateTimeField(
		db_column = "org_date_created",
		null=True, auto_now_add=True)
	org_feed_hash =  models.CharField(
		max_length=20,
		db_column = "org_feed_hash",
		verbose_name=_("Organization Feed Hash"),
		null=True, blank=True,)
	org_join_privacy = models.IntegerField(
		choices = ORG_JOIN_PRIVACY,
		default=0,
		verbose_name=_("Organization Join Privacy"),
		null=True, blank=True,)
	org_user_can_invite = models.BooleanField(
		verbose_name=_("Any Org Member can invite people to this org."),
		default=False)

	objects = OrganizationManager()

	#class Meta:
	#	db_table="Organizations"

	def __unicode__(self):
		return "%s" % (self.org_name)

	def get_events(self):
		if not hasattr(self, '_events'):
			self._events = self.event_set.filter(event_active=True)
		return self._events

	def get_eventtypes(self):
		return self.eventtype_set.filter(type_active=True)

	def get_org_groups(self):
		return self.group_set.all()

	def get_org_admin_groups(self):
		if not hasattr(self, '_org_admin_groups'):
			self._org_admin_groups = self.group_set.filter(admin_org=True)
		return self._org_admin_groups

	def get_coordinator_groups(self):
		if not hasattr(self, '_coordinator_groups'):
			self._coordinator_groups = self.group_set.filter(coord_events=True)
		return self._coordinator_groups

	def get_members(self):
		if not hasattr(self, '_members'):
			self._members = self.org_users.all()
		return self._members
	
	def get_member_count(self):
		if not hasattr(self, '_members'):
			self._members = self.org_users.all()
		return	self._members.count()
		

	def get_admin_users(self):
		from euser.models import User
		if not hasattr(self, '_admin_users'):
			self._admin_users =  User.objects.filter(user_groups__in=self.get_org_admin_groups())
		return self._admin_users
		#return self.get_members().filter(user_groups__in=self.get_org_admin_groups())
		# not sure if the commented syntax works.  Check
		
	def get_coordinator_users(self):
		from euser.models import User
		if not hasattr(self, '_coordinator_users'):
			self._coordinator_users = User.objects.filter(user_groups__in=self.get_coordinator_groups())
		return self._coordinator_users

	def get_current_event(self, event_hash, message=None):
		if message:
			return None, message
		else:
			try:
				return self.event_set.get(event_active=True, event_hash=event_hash), message
			except:
				current_event = None
				message = Message(title="Event Not Found", text="The event was not found")
			return current_event, message

	def get_absolute_url(self):
		return reverse('org_org_view',kwargs={'org_short_name':self.org_short_name,})

	def is_member(self,user):
		return self.org_users.filter(id=user.id)	

	def org_perms(self,user):
		permissions = {
		'can_add_event':False,   # user can create event in current org
		'can_remove_org':False,  # user can remove the current org
		'can_join_org':False,    # user can join the current org
		'can_edit_org':False,    # user can edit the current org
		'is_memberof_org':False, # user is a member of current org
		'can_add_type':False,    # user can add event type to current org
		'can_remove_type':False, # user can remove event type from current org
		'can_edit_type':False,   # user can edit event_type in current_rog
		'can_edit_group':False,  # user can edit the groups in the org
		'can_add_group':False,   # user can add groups to this org
		'can_remove_group':False, # user can remove groups in this org
		'can_remove_users':False, # user can remove users in theis org
		'can_invite_users':False, # user can invite users to theis org
		}

		permissions['is_memberof_org'] = self.is_member(user)
		if user.is_superuser == 1:
			permissions['can_add_event'] = True
			permissions['can_remove_org'] = True
			permissions['can_join_org'] = True
			permissions['can_edit_org'] = True
			permissions['can_add_type'] = True
			permissions['can_remove_type'] = True
			permissions['can_edit_type'] = True
			permissions['can_edit_group'] = True
			permissions['can_add_group'] = True
			permissions['can_remove_group'] = True
			permissions['can_remove_users'] = True
			permissions['can_invite_users'] = True
		elif self.get_admin_users().filter(id=user.id):
			permissions['can_add_event'] = True
			permissions['can_remove_org'] = True
			permissions['can_join_org'] = True
			permissions['can_edit_org'] = True
			permissions['can_add_type'] = True
			permissions['can_remove_type'] = True
			permissions['can_edit_type'] = True
			permissions['can_edit_group'] = True
			permissions['can_add_group'] = True
			permissions['can_remove_group'] = True
			permissions['can_remove_users'] = True
			permissions['can_invite_users'] = True			
		elif self.get_coordinator_users().filter(id=user.id):
			permissions['can_add_event'] = True
			permissions['can_join_org'] = True
			if self.org_join_privacy == 0:
				permissions['can_join_org'] = True	
			elif self.org_join_privacy == 1 or self.org_join_privacy == 2:
				from org.models import OrgInvite
				if  OrgInvite.objects.filter(org=self, user=user, direction=True) > 0:
					permissions['can_join_org'] = True
		else:
			if self.org_join_privacy == 0:
				permissions['can_join_org'] = True	
			if self.org_join_privacy == 1 or self.org_join_privacy == 2:
				from org.models import OrgInvite
				if  OrgInvite.objects.filter(org=self, user=user, direction=True) > 0:
					permissions['can_join_org'] = True
		
		if self.org_user_can_invite == True:
			permissions['can_invite_users'] = True
		
		return permissions

	def save(self):
		if len(str(self.org_feed_hash)) != 20:
			self.org_feed_hash = "".join(sample(KEYS,20))
		if not self.org_date_created:
			self.org_date_created = datetime.now()
		super(Organization, self).save()

class OrgInvite(models.Model):
	org = models.ForeignKey(Organization, related_name="invite_set")
	user = models.ForeignKey( User, blank=True, null=True, related_name="user_invites_set")
	email = models.EmailField(_(u'Anonymous email'), blank=True, null=True)
	direction = models.BooleanField(default=True)
	invite_hash = models.CharField(
		db_index=True,					
		max_length=20, verbose_name=_("Invite Hash"),
		null=True, blank=True,)
	
	def save(self):
		if len(str(self.invite_hash)) != 20:
			self.invite_hash = "".join(sample(KEYS,20))
		super(OrgInvite, self).save()
	
	def __unicode__(self):
		if self.user:
			return "%s invited to %s" % (self.user, self.org)
		else:
			return "%s invited to %s" % (self.email, self.org)
