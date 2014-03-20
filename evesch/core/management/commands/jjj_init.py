from datetime import datetime
from django.core.management.base import NoArgsCommand
from evesch.org.models import Organization
from evesch.egroup.models import UserGroup
from evesch.event.models import EventType, Event
from django.contrib.auth import get_user_model

class Command(NoArgsCommand):
	help = "Setup Users for Testing"
	def handle_noargs(self, **options):
		
		eusers = []
		
		#http://thingsilearned.com/2009/03/13/adding-custom-commands-to-managepy-and-django-adminpy/
		#from django.conf import settings
		#from django.core.management import setup_environ
		#setup_environ( settings )
	
		
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
		
		org3 = Organization(org_name='Northwestern University', org_short_name='nwu',)
		org3.org_desc = 'This is a private university'
		org3.org_phone = '312-555-1212'
		org3.org_email = 'nwu@evesch.com'
		org3.org_city = 'Chicago'
		org3.org_state = 'Illinois'
		org3.org_type = 4
		org3.save()
		print " Created: " + org3.org_name
		
		org4 = Organization(org_name='University of Chicago', org_short_name='uofc',)
		org4.org_desc = 'This is a private university'
		org4.org_phone = '312-555-1212'
		org4.org_email = 'uofc@evesch.com'
		org4.org_city = 'Chicago'
		org4.org_state = 'Illinois'
		org4.org_type = 4
		org4.save()
		print " Created: " + org4.org_name
		
		org5 = Organization(org_name='School of the Art Institute', org_short_name='ai',)
		org5.org_desc = 'This is a private university'
		org5.org_phone = '312-555-1212'
		org5.org_email = 'ai@evesch.com'
		org5.org_city = 'Chicago'
		org5.org_state = 'Illinois'
		org5.org_type = 4
		org5.save()
		print " Created: " + org5.org_name
		
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
		
		User = get_user_model()
		
		#Create custom users
		user_email='demo@evesch.com'
		euser = User(username="demo",email=user_email)
		euser.first_name='Demo'
		euser.last_name='Doe'
		euser.is_superuser=False
		euser.is_staff=False
		euser.set_password('demo')
		euser.save()
		euser.user_organizations=[org2]
		eusers.append(euser)
		print " Created: %s" % (euser.username)
				
		user_email='joe.jasinski@gmail.com'
		euser = User(username="joe",email=user_email)
		euser.first_name='joe'
		euser.last_name='jasinski'
		euser.is_superuser=True
		euser.is_staff=True
		euser.set_password('pl3ase')
		euser.save()
		euser.user_organizations=[org2]
		eusers.append(euser)
		print " Created: %s" % (euser.username)
		
		user_email='john.jasinski@gmail.com'
		euser = User(username="john",email=user_email)
		euser.first_name='john'
		euser.last_name='jasinski'
		euser.is_superuser=False
		euser.is_staff=False
		euser.set_password('1234')
		euser.save()
		euser.user_organizations=[org2]
		print " Created: %s" % (euser.username)
		
		
		usernames = [
					 'Jacinda','Jacinta','Jacinthe','Jacki','Jackie','Jacky','Jaclyn','Jacoba','Jacqueline',
					 'Jacqui','Jada','Jade','Jadwiga','Jael','Jaen','Jaffa','Jagrati','Jahnavi','Jaime',
					 'Jaimica','Jaimie','Jaina','Jaione','Jakinda','Jala','Jamal','Jamari','Jamee','Jamesina',
					 'Jamila','Jamilah','Jan','Jana','Jancis','Jane','Janelle','Janet','Janette','Janice',
					 'Janina','Janine','Janisa','Janna','Jannali','Janthina','Janthine','Japera','Jaquenetta',
					 'Jarah','Jardena','Jarita','Jarka','Jarmila','Jarrah','Jarvia','Jarvinia','Jasmine',
					 'Jaunie','Jaya','Jayani','Jayne','Jaythen','Jazlyn','Jean','Jeanne','Jeannette','Jehan',
					 'Jelena','Jemima','Jemma','Jena','Jenara','Jenay','Jendayi','Jendyose','Jenell','Jenica',
					 'Jenna','Jennifer','Jenny','Jeno','Jensine','Jeraldine','Jerarda','Jeremia','Jermain',
					 'Jermayne','Jerrica','Jerusha','Jesal','Jess','Jesse','Jessie','Jet','Jetta','Jewel',
					 'Jewell','Jezebel','Jezreel','Jiba','Jiera','Jigisha','Jihan','Jill','Jilli','Jillian',
					 'Jillie','Jilly','Jin','Jina','Jinx','Jirra','Joakima','Joan','Joann','Joanna','Joanne',
					 'Jobey','Jobina','Jocasta','Jocelyn','Jocosa','Jocunda','Jodi','Jodie','Joelle','Joelliane',
					 'Joesa','Johanna','Jolan','Jolanda','Jolanta','Jolene','Jolie','Jonesy','Joni','Jonie',
					 'Jonina','Jonquil','JooEun','Jora','Jordan','Jordana','Jordane','Joscelin','Josephine',
					 'Josie','Joslin','Josslyn','Jovita','Joy','Joyanne','Joyce','Juana','Juanita','Judith',
					 'Judy','Juene','Juhi','Jules','Julia','Juliana','Julianna','Julianne','Julie','Juliet',
					 'Julinka','Julya','Jumoke','Jun','June','Juniper','Juno','Justine','Jutta','Jutte','Jyoti',
					 'Jyotsna',
					 ]
		
		
		for username in usernames: 
			user_email = "%s.doe@evesch.com" % (username)
			euser = User(username=username, email=user_email)
			euser.first_name=username.capitalize()
			euser.last_name="Doe"
			euser.is_superuser = False
			euser.is_staff = False
			euser.set_password = "1234"
			euser.save()
			eusers.append(euser)
			print " Created: %s" % (euser.username)
			
		for euser in eusers:
			euser.user_organizations.add(org1)
			
		
		## Create some groups
		print "Creating Groups" 
		UserGroup.objects.init_org_groups(org1, eusers[1])
		g1 = UserGroup.objects.all()[0]
		eusers[2].user_groups.add(g1)
		eusers[0].user_groups.add(g1)
		UserGroup.objects.init_org_groups(org2, eusers[2])
		UserGroup.objects.init_org_groups(org3, eusers[2])
		UserGroup.objects.init_org_groups(org4, eusers[2])
		UserGroup.objects.init_org_groups(org5, eusers[2])
		
		## Create some events
		print "Creating Events" 
		event1 = Event.objects.create_event("IWU Event 1",eusers[1],org1,event_type1,datetime(2009,07,25,12,00,00))
		event1.event_desc = "This is event 1"
		event1.save()
		print " Created: " + event1.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name
		
		event2 = Event.objects.create_event("IWU Event 2",eusers[2],org1,event_type1,datetime(2009,07,14,12,00,00))
		event2.event_desc = "This is event 2"
		event2.save()
		print " Created: " + event2.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name
		
		event3 = Event.objects.create_event("IWU Event 3",eusers[2],org1,event_type1,datetime(2009,8,14,12,00,00))
		event3.event_desc = "This is event 3"
		event3.save()
		print " Created: " + event3.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name
		
		event4 = Event.objects.create_event("IWU Event 4",eusers[2],org1,event_type1,datetime(2009,9,14,12,00,00))
		event4.event_desc = "This is event 4"
		event4.save()
		print " Created: " + event4.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name
		
		event5 = Event.objects.create_event("IWU Event 5",eusers[1],org1,event_type1,datetime(2009,9,14,12,00,00))
		event5.event_desc = "This is event 5"
		event5.save()
		print " Created: " + event5.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name
		
		event6 = Event.objects.create_event("IWU Event 6",eusers[2],org1,event_type1,datetime(2009,9,14,12,00,00))
		event6.event_desc = "This is event 6"
		event6.save()
		print " Created: " + event6.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name
		
		
		
