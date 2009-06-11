from euser.models import User, UserEmail
from org.models import Organization
from event.models import EventType, Event
from datetime import datetime

# Create some orgs
print "---------------------"
print "Creating Orgs"
org1 = Organization(org_name='Illinois Wesleyan University', org_short_name='iwu',)
org1.org_desc = 'This is a liberal Arts School'
org1.org_phone = '309-555-1212'
org1.org_email = 'iwu@evesch.com'
org1.org_city = 'Bloomington'
org1.org_state = 'Illinois'
org1.org_type = 4
org1.save()
print " Created: " + org1.org_name

org2 = Organization(org_name='DePaul University', org_short_name='dpu',)
org2.org_desc = 'This is a private university'
org2.org_phone = '312-555-1212'
org2.org_email = 'dpu@evesch.com'
org2.org_city = 'Chicago'
org2.org_state = 'Illinois'
org2.org_type = 4
org2.save()
print " Created: " + org2.org_name

## Create some event types
print "Creating EventTypes"
event_type1 = EventType.objects.create_eventtype("Charity",org1)
event_type1.type_desc = "Charity Event"
event_type1.type_color = "00FF00"
event_type1.save()
print " Created: " + event_type1.type_name + " for org " + org1.org_short_name

event_type2 = EventType.objects.create_eventtype("Service",org2)
event_type2.type_desc = "Charity Event for Fun"
event_type2.type_color = "FF0000"
event_type2.save()
print " Created: " + event_type2.type_name + " for org " + org2.org_short_name

event_type3 = EventType.objects.create_eventtype("Community",org2)
event_type3.type_desc = "Charity Event for Fun"
event_type3.type_color = "0000FF"
event_type3.save()
print " Created: " + event_type2.type_name + " for org " + org2.org_short_name

## Create some users
print "Creating Users"
user_email = UserEmail(email_label = 'home', email_address='joe@evesch.com', email_isDefault=True)
user_email.save()
user1 = User(username="joe",email_addresses=user_email)
user1.first_name='joe'
user1.last_name='jasinski'
user1.is_superuser=True
user1.is_staff=True
user1.set_password('1234')
user1.save()
user1.user_organizations=[org2]
user1.user_organizations.add(org1)
print " Created: " + user1.username

user_email = UserEmail(email_label = 'jane', email_address='jane@evesch.com',email_isDefault=True)
user_email.save()
user2 = User(username='jane',email_addresses=user_email)
user2.first_name = 'Jane'
user2.last_name = 'Doe'
user2.is_superuser=True
user2.is_staff=True
user2.set_password('1234')
user2.save()
user2.user_organizations.add(org1)
print " Created: " + user2.username

user_email = UserEmail(email_label = 'jessica', email_address='jessica@evesch.com',email_isDefault=True)
user_email.save()
user3 = User(username='jessica',email_addresses=user_email)
user3.first_name = 'Jessica'
user3.last_name = 'Hot'
user3.is_superuser=True
user3.is_staff=False
user3.set_password('1234')
user3.save()
user3.user_organizations.add(org1)
print " Created: " + user3.username


## Create some events
print "Creating Events" 
event1 = Event.objects.create_event("IWU Event 1",user1,org1,event_type1,datetime(2009,02,25,12,00,00))
event1.save()
print " Created: " + event1.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name

#user = User.objects.create_user('joe','joe@evesch.com','1234')
#user.is_superuser=True
#user.save()
