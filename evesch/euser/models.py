from random import sample
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from evesch.org.models import Organization
from evesch.egroup.models import UserGroup
from evesch.core.lib import Message


KEYS='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

PRIVACY_TYPES = (
           (1,u'All_View'),
           (2,u'Org_View'),
           (3,u'Event_View'),     
                )

def get_current_user_by_email(email, message=None):
    if message:
        return None, message
    else:
        try:
            current_user = get_user_model().objects.get(email=email)
        except:
            current_user = None
            message = Message(title=_("User Not Found"), text=_("The user was not found. Are you logged in?"))
        return current_user, message


class UserIM(models.Model):

    IM_PROTOCOL_TYPES = (
        (1,u'AIM'),
        (2,u'Bonjour'),
        (3,u'Google Talk'),
        (4,u'ICQ'),
        (5,u'IRC'),
        (6,u'Skype'),
        (7,u'Jabber'),
        (8,u'QQ'),
        (9,u'Windows Messenger'),
        (10,u'Yahoo Messenger'),
    )
    
    im_name = models.CharField(
        verbose_name = _("Instant Messenger Name"), 
        max_length=48)
    im_protocol_type = models.IntegerField(
        verbose_name = _("Instant Messenger Protocol Type"), 
        choices=IM_PROTOCOL_TYPES)
    im_privacy = models.IntegerField(
        verbose_name = _("Instant Messenger Privacy"), 
        choices=PRIVACY_TYPES)
    im_isDefault = models.BooleanField(
        verbose_name = _("Is IM Default Name"), 
        default=False)
    
    def __str__(self):
        return "%s - %s" % (self.im_name, self.im_protocol_type)


class eUser(AbstractUser):
    GENDER_CHOICES = (
        (1,u'Male'),
        (2,u'Female'),
        (3,u'Other'),
    )

    user_organizations = models.ManyToManyField(Organization, 
        related_name="org_users",
        verbose_name=_("User Organizations"),                                    
        blank=True)
    user_groups = models.ManyToManyField(UserGroup,
        verbose_name=_("User Groups"),
        related_name="group_users",
        blank=True)
    phone = models.CharField(
        verbose_name=_("Phone Number"),
        max_length=64, 
        blank=True, null=True)
    gender = models.IntegerField(
        verbose_name=_("Gender"),
        choices=GENDER_CHOICES, 
        blank=True, null=True, 
        help_text=_("Optional Gender Information"))
    country = models.CharField(
        verbose_name=_("Country"),
        max_length=64,
        help_text=_("User's Country"),
        blank=True, null=True)
    city = models.CharField(
        verbose_name=_("City"),
        blank=True, null=True,
        max_length=64,
        help_text=_("User's City"))
    im_names = models.ForeignKey(
        UserIM,
        related_name=u"user_im_names",
        blank=True, null=True,
        on_delete=models.CASCADE) 
    about = models.CharField(
        verbose_name=_("About Me"),
        max_length=256,
        blank=True, null=True)
    security_hash = models.CharField(
        verbose_name=_("Confirmation Number"),
        blank=True, null=True,
        max_length=24)
    user_feed_hash =  models.CharField(
        max_length=24,
        verbose_name=_("User Feed Hash"),
        null=True, blank=True,)

    def __str__(self):
        return "%s" % (self.username)
    
    def get_user_orgs(self):
        return self.user_organizations.filter(org_active=True)

    def get_user_groups(self):
        return self.user_groups.all()
    
    def get_attending_events(self):
        return self.attendee_set.all()
    
    def get_org_invites(self):
        return self.user_invites_set.all()

    def get_org_invites_count(self):
        return self.user_invites_set.count()

    def set_password(self, raw_password):
        super(eUser, self).set_password(raw_password)

    def get_absolute_url(self):
        return reverse('euser_user_view', kwargs={'username':self.username,})

    def save(self, *args, **kwargs):
        if not self.id:
            self.user_feed_hash = "".join(sample(KEYS,24))
        super(eUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


def get_current_user(username, message=None):
    if message:
        return None, message
    else:
        try:
            current_user = eUser.objects.get(username=username)
        except:
            current_user = None
            message = Message(
                title=_("User Not Found"),
                text=_("The user was not found. Are you logged in?"))
        return current_user, message