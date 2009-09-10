from django.db import models
from org.models import Organization
from euser.models import User
from datetime import datetime
from random import sample
from core.exceptions import EventTypeExistsException
from core.middleware import threadlocals 
from django.utils.translation import ugettext_lazy as _
from core.lib import text_vs_bg
from django.core.urlresolvers import reverse
#from django.contrib.auth.models import User

KEYS='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class EventTypeManager(models.Manager):
	def create_eventtype(self, type_name, org_name, type_desc=None, type_color=None):
		if EventType.objects.filter(type_name=type_name, org_name=org_name, type_active=True).count() < 1:
			event_type = EventType(type_name=type_name, org_name=org_name)
			event_type.type_desc = type_desc
			event_type.type_color = type_color
			event_type.save()
			return event_type
		else:
			raise EventTypeExistsException('Type already exists')
	
	def init_event_types(self, org_name):
		return self.create_eventtype("Default", org_name, "Default Type", "FF0000")
		

class EventType(models.Model):
	type_name = models.CharField(
		db_column = "type_name",
		verbose_name=_("Event Type"),
		#db_index=True,
		unique=False,
		max_length=64)
	type_hash = models.CharField(
		db_column = "type_hash",
		verbose_name=_("Event Type Hash"),
		db_index=True,
		unique=True,
		max_length=8,)
	type_desc = models.CharField(
		db_column = "type_desc",
		verbose_name=_("Event Type Description"),
		max_length=256, 
		blank=True, null=True)
	type_color = models.CharField(
		verbose_name=_("Event Type Color"),
		max_length=15, 
		blank=True, null=True)
	type_track_hours = models.BooleanField(
		db_column="type_track_hours",
		verbose_name=_("Track Hours for events of this type?"),
		default = False)
	org_name = models.ForeignKey(Organization)
	type_active = models.BooleanField(
		verbose_name = _("Event Type Enabled"),
		help_text = _("Has the event been disabled?"),
		default=True)
	objects = EventTypeManager()
    
	def contrast(self):
	   return text_vs_bg(self.type_color)

	def save(self):
		if not self.id:
			self.type_hash =  "".join(sample(KEYS,8))
		super(EventType, self).save()
		
	objects = EventTypeManager()

	def get_events(self):
		if not hasattr(self, '_events'):
			self._events = self.event_set.filter(event_active=True)
		return self._events

	#class Meta:
	#	db_table="EventTypes"

	def __unicode__(self):
		return "%s" % (self.type_name)
	
class EventManager(models.Manager):
	def create_event(self, event_name,event_creator_name,
					 event_org,event_type,event_date):
		event = Event(event_name=event_name,
					  event_creator_name=event_creator_name,
					  event_org=event_org,
					  event_type=event_type,
					  event_date=event_date)
		return event
		
class Event(models.Model):
	event_name = models.CharField(
		db_column="event_name",
		verbose_name=_("Event Name"),
		db_index=True,
		max_length=64)
	event_hash = models.CharField(
		db_column = "event_hash",
		verbose_name=_("Event Hash"),
		db_index=True,
		unique=True,
		max_length=8,)
	event_active = models.NullBooleanField(
		db_column="event_active",
		verbose_name=_("Does the Event Exist?"),
		default = True, blank=True, null=True)
	event_open = models.BooleanField(
		db_column="event_open",
		verbose_name=_("Event open to Add Attendees"),
		default=True)
	event_signup_deadline = models.DateTimeField(
		db_column = "event_signup_deadline",
		verbose_name = _("Date that you must register by."),
		blank=True, null=True)
	event_date = models.DateTimeField(
		db_column="event_date",
		db_index=True,
		verbose_name=_("Date and Time of Event"))
	event_creator_name = models.ForeignKey(User,
		db_column="event_creator_name",
		verbose_name=_("Event Creator"), related_name="event_creator")
	event_created_date = models.DateTimeField(
		db_column="event_created_date",
		verbose_name=_("Event Created Date"),
		null=True, auto_now_add=True)
	event_desc = models.CharField(
		db_column="event_desc",
		verbose_name=_("Event Description"),
		max_length=512, blank=True, null=True)
	event_max_attendees = models.IntegerField(
		db_column="event_max_attendees",
		verbose_name=_("Maximum Number of Addendees"),
		blank=True, null=True)
	event_priority = models.IntegerField(
		db_column="event_priority",
		verbose_name=_("Event Priority"),
		blank=True, null=True)	
	event_type = models.ForeignKey(EventType, 
		verbose_name=_("Type of Event"))
	event_org = models.ForeignKey(Organization, 
		verbose_name=_("Organization Sponsoring the Event"))
	event_coordinators = models.ManyToManyField(User,
		verbose_name=_("Event Coordinators"))
	event_track_hours = models.BooleanField(
		verbose_name=_("Should we track the hours attendees spend at events?"),
		default=False)
	att_header_col1 = models.CharField(
		max_length=20,
		verbose_name=_("Column 1 Header"),
		blank=True, null=True,)
	att_require_col1 = models.BooleanField(u'Required',default=False)
	att_header_col2 = models.CharField(
		max_length=20,
		verbose_name=_("Column 2 Header"),
		blank=True, null=True,)
	att_require_col2 = models.BooleanField(u'Required',default=False)
	att_header_col3 = models.CharField(
		max_length=20,
		verbose_name=_("Column 3 Header"),
		blank=True, null=True,)
	att_require_col3 = models.BooleanField(u'Required',default=False)
	att_header_col4 = models.CharField(
		max_length=20,
		verbose_name=_("Column 4 Header"),
		blank=True, null=True,)
	att_require_col4 = models.BooleanField(u'Required',default=False)
	att_header_col5 = models.CharField(
		max_length=20,
		verbose_name=_("Column 5 Header"),
		blank=True, null=True,)
	att_require_col5 = models.BooleanField(u'Required',default=False)
	att_header_col6 = models.CharField(
		max_length=20,
		verbose_name=_("Column 6 Header"),
		blank=True, null=True,)	
	att_require_col6 = models.BooleanField(u'Required',default=False)
	objects = EventManager()
	#class Meta:
	#	db_table="Events"

	def is_within_signup_deadline(self):
		if self.event_signup_deadline < datetime.now():
			return False
		else:
			return True
	
	def is_past(self):
		if self.event_date < datetime.now():
			return False
		else:
			return True

	def __unicode__(self):
		return "%s" % (self.event_name)
	
	def get_attendees(self):
		return self.attendee_set.all()
	
	def get_attendee_count(self):
		return self.attendee_set.count()
	
	def get_event_coordinators(self):
		return self.event_coordinators.all()

	def is_attending(self, user):
		return self.attendee_set.filter(att_name=user)
	
	def is_event_coordinator(self,user):
		return self.event_coordinators.filter(username=user)

	def is_creator(self,user):
		if self.event_creator_name.id == user.id:
			return True
		else:
		    return False
	
	def get_absolute_url(self):
		return reverse('event_event_view',kwargs={'org_short_name':self.event_org.org_short_name,'event_hash':self.event_hash})
	
	def is_additional_signup_info(self):
		return self.att_header_col1 or self.att_header_col2 or self.att_header_col3 or self.att_header_col4 or self.att_header_col5 or self.att_header_col6 or self.event_track_hours
	
	def event_perms(self, user=False):
		permissions = {
	        'can_remove_event':False,
	        'can_edit_event':False,
	        'can_join_event':True,
	        'is_attending_event':False,
	        'can_message_event':False,
	        }
		if not user:
			user=threadlocals.get_current_user()
		if user:
		    operms = self.event_org.org_perms()
		    permissions['is_attending_event'] = self.is_attending(user)
		    if user.is_superuser == 1:
		    	if operms['is_memberof_org']:
			        permissions['can_remove_event'] = True
			        permissions['can_edit_event'] = True
			        permissions['can_message_event'] = True
			        permissions['can_join_event'] = True
		    if self.event_org.get_admin_users().filter(id=user.id):
		    	if operms['is_memberof_org']:
			        permissions['can_remove_event'] = True
			        permissions['can_edit_event'] = True
			        permissions['can_message_event'] = True
			        permissions['can_join_event'] = True		    	
		    else: 
		    	if operms['is_memberof_org']:
			        permissions['can_remove_event'] = self.is_event_coordinator(user) or self.is_creator(user)
			        permissions['can_edit_event'] = self.is_event_coordinator(user) or self.is_creator(user)
			        permissions['can_message_event'] = permissions['is_attending_event']
			
		return permissions
	
	
	def save(self):
		if not self.id:
			self.event_hash = "".join(sample(KEYS,8))
			if not self.event_signup_deadline:
				self.event_signup_deadline = self.event_date
			if not self.event_desc:
				self.event_desc = ""
		super(Event, self).save()

class AttendeeManager(models.Manager):
	def exists(self, attendee):
		pass

class Attendee(models.Model):
	att_name = models.ForeignKey(User, 
		verbose_name=_("User Attending"))
	att_event = models.ForeignKey(Event,
		#related_name="event_attendees",
		verbose_name=_("Event to Attend"))
	att_added_date = models.DateTimeField(
		db_column="att_added_date",
		verbose_name=_("Register Date"), 
		auto_now_add=True)
	att_ip = models.IPAddressField(
		db_column="att_ip",
		verbose_name=_("Attendee IP Address"),
		blank=True, null=True,)
	att_hours = models.FloatField(
		db_column="att_hours",
		verbose_name=_("Attendee Hours"),
		blank=True, null=True,)
	att_col1 = models.CharField(
		max_length=20,
		verbose_name=_("Column 1"),
		blank=True, null=True,)
	att_col2 = models.CharField(
		max_length=20,
		verbose_name=_("Column 2"),
		blank=True, null=True,)
	att_col3 = models.CharField(
		max_length=20,
		verbose_name=_("Column 3"),
		blank=True, null=True,)
	att_col4 = models.CharField(
		max_length=20,
		verbose_name=_("Column 4"),
		blank=True, null=True,)
	att_col5 = models.CharField(
		max_length=20,
		verbose_name=_("Column 5"),
		blank=True, null=True,)
	att_col6 = models.CharField(
		max_length=20,
		verbose_name=_("Column 6"),
		blank=True, null=True,)
	objects = AttendeeManager()
	
	#def is_registered(self, user, event):
	#	try: 
	#		self.objects.get(att_name=user,att_event=event)
	#		return True
	#	except:
	#		return False
		
	#class Meta:
	#	db_table="Attendees"
	def is_attending(self, user):
		return self.att_name.id == user.user.id

	def __unicode__(self):
		return "%s" % (self.att_name)

	#def display_users(self):
	#	return "%s - %s" % (threadlocals.get_current_user().user.id, self.att_name.id)

	#def __int__(self):
	#	return self.id
	
	def att_perms(self, user=None):
		permissions = {
	        'can_remove_attendee':False,  
	        'can_remove_attendee_after_event':False,         
	        }
		if not user:
			user=threadlocals.get_current_user()
		if user:
			event = self.att_event

			if user.is_superuser == 1:
				permissions['can_remove_attendee'] = True
				permissions['can_remove_attendee_after_event'] = True
			elif event.event_org.get_admin_users().filter(id=user.id):
				permissions['can_remove_attendee'] = True
				permissions['can_remove_attendee_after_event'] = True
			elif event.is_creator(user) or event.is_event_coordinator(user):
				permissions['can_remove_attendee'] = True
				permissions['can_remove_attendee_after_event'] = True
			else:
				permissions['can_remove_attendee'] = self.is_attending(user)
		return permissions
