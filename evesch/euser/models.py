from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from org.models import Organization
from egroup.models import UserGroup
from core.lib import Message

PRIVACY_TYPES = (
           (1,u'All_View'),
           (2,u'Org_View'),
           (3,u'Event_View'),     
                )


def get_current_user(username, message=None):
    if message:
        return None, message
    else:
        try:
            current_user = User.objects.get(username=username)
        except:
            current_user = None
            message = Message(title=_("User Not Found"), text=_("The user was not found. Are you logged in?"))
        return current_user, message


class UserEmail(models.Model):

    EMAIL_TYPES = (
        (1,u'Personal'),
        (2,u'Work'),
    )

    email_label = models.CharField(max_length=15)    
    email_address = models.EmailField()
    email_type = models.IntegerField(choices=EMAIL_TYPES,default=1)
    email_privacy = models.IntegerField(choices=PRIVACY_TYPES,default=2)
    email_isDefault = models.BooleanField(
        verbose_name=_("Is Default Email"), 
        default=False)
    
    def __unicode__(self):
        return "%s <%s>" % (self.email_label, self.email_address)

    
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
    
    def __unicode__(self):
        return "%s - %s" % (self.im_name, self.im_protocol_type)


class User(User):
    GENDER_CHOICES = (
        (0,u'Male'),
        (1,u'Female'),
    )

    last_name = models.CharField(
        db_column=u"last_name",
        verbose_name=_("Last Name"),
        #db_index=True,
        #unique=False,
        max_length=48, 
        null=True, blank=True)
    first_name = models.CharField(
        db_column=u"first_name",
        verbose_name=_("First Name"),
        #db_index=True,
        #unique=False,
        max_length=48, 
        null=True, blank=True)
    user_organizations = models.ManyToManyField(Organization, 
        related_name = "org_users",
        verbose_name = _("User Organizations"),                                    
        blank=True, null=True)
    user_groups = models.ManyToManyField(UserGroup,
        verbose_name = _("User Groups"),
        blank=True, null=True)
    phone = models.CharField(
        db_column=u"phone",
        verbose_name=_("Phone Number"),
        max_length=64, 
        blank=True, null=True)
    gender = models.IntegerField(
        db_column = u"gender",
        verbose_name= _("Gender"),
        choices=GENDER_CHOICES, 
        blank=True, null=True, 
        help_text = _("Optional Gender Information"))
    email_addresses = models.ForeignKey(UserEmail,
        related_name = "user_email_addresses")
    country = models.CharField(
        verbose_name = _("Country"),
        max_length=64,
        help_text = _("User's Country"),
        blank=True,null=True)
    city = models.CharField(
        verbose_name = _("City"),
        blank=True,null=True,
        max_length=64,
        help_text = _("User's City"))
    im_names = models.ForeignKey(UserIM,
        related_name = u"user_im_names",                   
        blank=True,null=True) 
    about = models.CharField(
        db_column = u"about",
        verbose_name = _("About Me"),
        max_length=256,
        blank=True, null=True)
    objects = UserManager()
    
   # class Meta:
    #    db_table="EveschUsers"

    def __unicode__(self):
        return "%s" % (self.username)
    
    def get_user_orgs(self):
        return self.user_organizations.filter(org_active=True)

    def get_user_groups(self):
        return self.user_groups.all()
    
    def get_attending_events(self):
        return self.attendee_set.all()
        
    def save(self):
        super(User, self).save()

    def set_password(self, raw_password):
        super(User, self).set_password(raw_password)