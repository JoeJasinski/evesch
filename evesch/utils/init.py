from euser.models import User
from org.models import Organization
from egroup.models import UserGroup
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


user_email='demo@evesch.com'
user0 = User(username="demo",email=user_email)
user0.first_name='Demo'
user0.last_name='Doe'
user0.is_superuser=False
user0.is_staff=False
user0.set_password('demo')
user0.save()
user0.user_organizations=[org2]
user0.user_organizations.add(org1)

user_email='joe.jasinski@gmail.com'
user1 = User(username="joe",email=user_email)
user1.first_name='joe'
user1.last_name='jasinski'
user1.is_superuser=True
user1.is_staff=True
user1.set_password('pl3ase')
user1.save()
user1.user_organizations=[org2]
user1.user_organizations.add(org1)
print " Created: " + user1.username

user_email='john.jasinski@gmail.com'
user2 = User(username="john",email=user_email)
user2.first_name='john'
user2.last_name='jasinski'
user2.is_superuser=False
user2.is_staff=False
user2.set_password('1234')
user2.save()
user2.user_organizations=[org2]
user2.user_organizations.add(org1)
print " Created: " + user2.username


user_email="jacinda.hot@evesch.com"
user3 = User(username='jacinda',email=user_email)
user3.first_name = 'Jacinda'
user3.last_name = 'Hot'
user3.is_superuser=False
user3.is_staff=False
user3.set_password('1234')
user3.save()
user3.user_organizations.add(org1)
user3.user_organizations.add(org2)
print ' Created: ' + user3.username
user_email="jacinta.hot@evesch.com"
user4 = User(username='jacinta',email=user_email)
user4.first_name = 'Jacinta'
user4.last_name = 'Hot'
user4.is_superuser=False
user4.is_staff=False
user4.set_password('1234')
user4.save()
user4.user_organizations.add(org1)
user4.user_organizations.add(org2)
print ' Created: ' + user4.username
user_email="jacinthe.hot@evesch.com"
user5 = User(username='jacinthe',email=user_email)
user5.first_name = 'Jacinthe'
user5.last_name = 'Hot'
user5.is_superuser=False
user5.is_staff=False
user5.set_password('1234')
user5.save()
user5.user_organizations.add(org1)
user5.user_organizations.add(org2)
print ' Created: ' + user5.username
user_email="jacki.hot@evesch.com"
user6 = User(username='jacki',email=user_email)
user6.first_name = 'Jacki'
user6.last_name = 'Hot'
user6.is_superuser=False
user6.is_staff=False
user6.set_password('1234')
user6.save()
user6.user_organizations.add(org1)
user6.user_organizations.add(org2)
print ' Created: ' + user6.username
user_email="jackie.hot@evesch.com"
user7 = User(username='jackie',email=user_email)
user7.first_name = 'Jackie'
user7.last_name = 'Hot'
user7.is_superuser=False
user7.is_staff=False
user7.set_password('1234')
user7.save()
user7.user_organizations.add(org1)
print ' Created: ' + user7.username
user_email="jacky.hot@evesch.com"
user8 = User(username='jacky',email=user_email)
user8.first_name = 'Jacky'
user8.last_name = 'Hot'
user8.is_superuser=False
user8.is_staff=False
user8.set_password('1234')
user8.save()
user8.user_organizations.add(org1)
print ' Created: ' + user8.username
user_email="jaclyn.hot@evesch.com"
user9 = User(username='jaclyn',email=user_email)
user9.first_name = 'Jaclyn'
user9.last_name = 'Hot'
user9.is_superuser=False
user9.is_staff=False
user9.set_password('1234')
user9.save()
user9.user_organizations.add(org1)
print ' Created: ' + user9.username
user_email="jacoba.hot@evesch.com"
user10 = User(username='jacoba',email=user_email)
user10.first_name = 'Jacoba'
user10.last_name = 'Hot'
user10.is_superuser=False
user10.is_staff=False
user10.set_password('1234')
user10.save()
user10.user_organizations.add(org1)
print ' Created: ' + user10.username
user_email="jacqueline.hot@evesch.com"
user11 = User(username='jacqueline',email=user_email)
user11.first_name = 'Jacqueline'
user11.last_name = 'Hot'
user11.is_superuser=False
user11.is_staff=False
user11.set_password('1234')
user11.save()
user11.user_organizations.add(org1)
print ' Created: ' + user11.username
user_email="jacqui.hot@evesch.com"
user12 = User(username='jacqui',email=user_email)
user12.first_name = 'Jacqui'
user12.last_name = 'Hot'
user12.is_superuser=False
user12.is_staff=False
user12.set_password('1234')
user12.save()
user12.user_organizations.add(org1)
print ' Created: ' + user12.username
user_email="jada.hot@evesch.com"
user13 = User(username='jada',email=user_email)
user13.first_name = 'Jada'
user13.last_name = 'Hot'
user13.is_superuser=False
user13.is_staff=False
user13.set_password('1234')
user13.save()
user13.user_organizations.add(org1)
print ' Created: ' + user13.username
user_email="jade.hot@evesch.com"
user14 = User(username='jade',email=user_email)
user14.first_name = 'Jade'
user14.last_name = 'Hot'
user14.is_superuser=False
user14.is_staff=False
user14.set_password('1234')
user14.save()
user14.user_organizations.add(org1)
print ' Created: ' + user14.username
user_email="jadwiga.hot@evesch.com"
user15 = User(username='jadwiga',email=user_email)
user15.first_name = 'Jadwiga'
user15.last_name = 'Hot'
user15.is_superuser=False
user15.is_staff=False
user15.set_password('1234')
user15.save()
user15.user_organizations.add(org1)
print ' Created: ' + user15.username
user_email="jael.hot@evesch.com"
user16 = User(username='jael',email=user_email)
user16.first_name = 'Jael'
user16.last_name = 'Hot'
user16.is_superuser=False
user16.is_staff=False
user16.set_password('1234')
user16.save()
user16.user_organizations.add(org1)
print ' Created: ' + user16.username
user_email="jaen.hot@evesch.com"
user17 = User(username='jaen',email=user_email)
user17.first_name = 'Jaen'
user17.last_name = 'Hot'
user17.is_superuser=False
user17.is_staff=False
user17.set_password('1234')
user17.save()
user17.user_organizations.add(org1)
print ' Created: ' + user17.username
user_email="jaffa.hot@evesch.com"
user18 = User(username='jaffa',email=user_email)
user18.first_name = 'Jaffa'
user18.last_name = 'Hot'
user18.is_superuser=False
user18.is_staff=False
user18.set_password('1234')
user18.save()
user18.user_organizations.add(org1)
print ' Created: ' + user18.username
user_email="jagrati.hot@evesch.com"
user19 = User(username='jagrati',email=user_email)
user19.first_name = 'Jagrati'
user19.last_name = 'Hot'
user19.is_superuser=False
user19.is_staff=False
user19.set_password('1234')
user19.save()
user19.user_organizations.add(org1)
print ' Created: ' + user19.username
user_email="jahnavi.hot@evesch.com"
user20 = User(username='jahnavi',email=user_email)
user20.first_name = 'Jahnavi'
user20.last_name = 'Hot'
user20.is_superuser=False
user20.is_staff=False
user20.set_password('1234')
user20.save()
user20.user_organizations.add(org1)
print ' Created: ' + user20.username
user_email="jaime.hot@evesch.com"
user21 = User(username='jaime',email=user_email)
user21.first_name = 'Jaime'
user21.last_name = 'Hot'
user21.is_superuser=False
user21.is_staff=False
user21.set_password('1234')
user21.save()
user21.user_organizations.add(org1)
print ' Created: ' + user21.username
user_email="jaimica.hot@evesch.com"
user22 = User(username='jaimica',email=user_email)
user22.first_name = 'Jaimica'
user22.last_name = 'Hot'
user22.is_superuser=False
user22.is_staff=False
user22.set_password('1234')
user22.save()
user22.user_organizations.add(org1)
print ' Created: ' + user22.username
user_email="jaimie.hot@evesch.com"
user23 = User(username='jaimie',email=user_email)
user23.first_name = 'Jaimie'
user23.last_name = 'Hot'
user23.is_superuser=False
user23.is_staff=False
user23.set_password('1234')
user23.save()
user23.user_organizations.add(org1)
print ' Created: ' + user23.username
user_email="jaina.hot@evesch.com"
user24 = User(username='jaina',email=user_email)
user24.first_name = 'Jaina'
user24.last_name = 'Hot'
user24.is_superuser=False
user24.is_staff=False
user24.set_password('1234')
user24.save()
user24.user_organizations.add(org1)
print ' Created: ' + user24.username
user_email="jaione.hot@evesch.com"
user25 = User(username='jaione',email=user_email)
user25.first_name = 'Jaione'
user25.last_name = 'Hot'
user25.is_superuser=False
user25.is_staff=False
user25.set_password('1234')
user25.save()
user25.user_organizations.add(org1)
print ' Created: ' + user25.username
user_email="jakinda.hot@evesch.com"
user26 = User(username='jakinda',email=user_email)
user26.first_name = 'Jakinda'
user26.last_name = 'Hot'
user26.is_superuser=False
user26.is_staff=False
user26.set_password('1234')
user26.save()
user26.user_organizations.add(org1)
print ' Created: ' + user26.username
user_email="jala.hot@evesch.com"
user27 = User(username='jala',email=user_email)
user27.first_name = 'Jala'
user27.last_name = 'Hot'
user27.is_superuser=False
user27.is_staff=False
user27.set_password('1234')
user27.save()
user27.user_organizations.add(org1)
print ' Created: ' + user27.username
user_email="jamal.hot@evesch.com"
user28 = User(username='jamal',email=user_email)
user28.first_name = 'Jamal'
user28.last_name = 'Hot'
user28.is_superuser=False
user28.is_staff=False
user28.set_password('1234')
user28.save()
user28.user_organizations.add(org1)
print ' Created: ' + user28.username
user_email="jamari.hot@evesch.com"
user29 = User(username='jamari',email=user_email)
user29.first_name = 'Jamari'
user29.last_name = 'Hot'
user29.is_superuser=False
user29.is_staff=False
user29.set_password('1234')
user29.save()
user29.user_organizations.add(org1)
print ' Created: ' + user29.username
user_email="jamee.hot@evesch.com"
user30 = User(username='jamee',email=user_email)
user30.first_name = 'Jamee'
user30.last_name = 'Hot'
user30.is_superuser=False
user30.is_staff=False
user30.set_password('1234')
user30.save()
user30.user_organizations.add(org1)
print ' Created: ' + user30.username
user_email="jamesina.hot@evesch.com"
user31 = User(username='jamesina',email=user_email)
user31.first_name = 'Jamesina'
user31.last_name = 'Hot'
user31.is_superuser=False
user31.is_staff=False
user31.set_password('1234')
user31.save()
user31.user_organizations.add(org1)
print ' Created: ' + user31.username
user_email="jamila.hot@evesch.com"
user32 = User(username='jamila',email=user_email)
user32.first_name = 'Jamila'
user32.last_name = 'Hot'
user32.is_superuser=False
user32.is_staff=False
user32.set_password('1234')
user32.save()
user32.user_organizations.add(org1)
print ' Created: ' + user32.username
user_email="jamilah.hot@evesch.com"
user33 = User(username='jamilah',email=user_email)
user33.first_name = 'Jamilah'
user33.last_name = 'Hot'
user33.is_superuser=False
user33.is_staff=False
user33.set_password('1234')
user33.save()
user33.user_organizations.add(org1)
print ' Created: ' + user33.username
user_email="jan.hot@evesch.com"
user34 = User(username='jan',email=user_email)
user34.first_name = 'Jan'
user34.last_name = 'Hot'
user34.is_superuser=False
user34.is_staff=False
user34.set_password('1234')
user34.save()
user34.user_organizations.add(org1)
print ' Created: ' + user34.username
user_email="jana.hot@evesch.com"
user35 = User(username='jana',email=user_email)
user35.first_name = 'Jana'
user35.last_name = 'Hot'
user35.is_superuser=False
user35.is_staff=False
user35.set_password('1234')
user35.save()
user35.user_organizations.add(org1)
print ' Created: ' + user35.username
user_email="jancis.hot@evesch.com"
user36 = User(username='jancis',email=user_email)
user36.first_name = 'Jancis'
user36.last_name = 'Hot'
user36.is_superuser=False
user36.is_staff=False
user36.set_password('1234')
user36.save()
user36.user_organizations.add(org1)
print ' Created: ' + user36.username
user_email="jane.hot@evesch.com"
user37 = User(username='jane',email=user_email)
user37.first_name = 'Jane'
user37.last_name = 'Hot'
user37.is_superuser=False
user37.is_staff=False
user37.set_password('1234')
user37.save()
user37.user_organizations.add(org1)
print ' Created: ' + user37.username
user_email="janelle.hot@evesch.com"
user38 = User(username='janelle',email=user_email)
user38.first_name = 'Janelle'
user38.last_name = 'Hot'
user38.is_superuser=False
user38.is_staff=False
user38.set_password('1234')
user38.save()
user38.user_organizations.add(org1)
print ' Created: ' + user38.username
user_email="janet.hot@evesch.com"
user39 = User(username='janet',email=user_email)
user39.first_name = 'Janet'
user39.last_name = 'Hot'
user39.is_superuser=False
user39.is_staff=False
user39.set_password('1234')
user39.save()
user39.user_organizations.add(org1)
print ' Created: ' + user39.username
user_email="janette.hot@evesch.com"
user40 = User(username='janette',email=user_email)
user40.first_name = 'Janette'
user40.last_name = 'Hot'
user40.is_superuser=False
user40.is_staff=False
user40.set_password('1234')
user40.save()
user40.user_organizations.add(org1)
print ' Created: ' + user40.username
user_email="janice.hot@evesch.com"
user41 = User(username='janice',email=user_email)
user41.first_name = 'Janice'
user41.last_name = 'Hot'
user41.is_superuser=False
user41.is_staff=False
user41.set_password('1234')
user41.save()
user41.user_organizations.add(org1)
print ' Created: ' + user41.username
user_email="janina.hot@evesch.com"
user42 = User(username='janina',email=user_email)
user42.first_name = 'Janina'
user42.last_name = 'Hot'
user42.is_superuser=False
user42.is_staff=False
user42.set_password('1234')
user42.save()
user42.user_organizations.add(org1)
print ' Created: ' + user42.username
user_email="janine.hot@evesch.com"
user43 = User(username='janine',email=user_email)
user43.first_name = 'Janine'
user43.last_name = 'Hot'
user43.is_superuser=False
user43.is_staff=False
user43.set_password('1234')
user43.save()
user43.user_organizations.add(org1)
print ' Created: ' + user43.username
user_email="janisa.hot@evesch.com"
user44 = User(username='janisa',email=user_email)
user44.first_name = 'Janisa'
user44.last_name = 'Hot'
user44.is_superuser=False
user44.is_staff=False
user44.set_password('1234')
user44.save()
user44.user_organizations.add(org1)
print ' Created: ' + user44.username
user_email="janna.hot@evesch.com"
user45 = User(username='janna',email=user_email)
user45.first_name = 'Janna'
user45.last_name = 'Hot'
user45.is_superuser=False
user45.is_staff=False
user45.set_password('1234')
user45.save()
user45.user_organizations.add(org1)
print ' Created: ' + user45.username
user_email="jannali.hot@evesch.com"
user46 = User(username='jannali',email=user_email)
user46.first_name = 'Jannali'
user46.last_name = 'Hot'
user46.is_superuser=False
user46.is_staff=False
user46.set_password('1234')
user46.save()
user46.user_organizations.add(org1)
print ' Created: ' + user46.username
user_email="janthina.hot@evesch.com"
user47 = User(username='janthina',email=user_email)
user47.first_name = 'Janthina'
user47.last_name = 'Hot'
user47.is_superuser=False
user47.is_staff=False
user47.set_password('1234')
user47.save()
user47.user_organizations.add(org1)
print ' Created: ' + user47.username
user_email="janthine.hot@evesch.com"
user48 = User(username='janthine',email=user_email)
user48.first_name = 'Janthine'
user48.last_name = 'Hot'
user48.is_superuser=False
user48.is_staff=False
user48.set_password('1234')
user48.save()
user48.user_organizations.add(org1)
print ' Created: ' + user48.username
user_email="japera.hot@evesch.com"
user49 = User(username='japera',email=user_email)
user49.first_name = 'Japera'
user49.last_name = 'Hot'
user49.is_superuser=False
user49.is_staff=False
user49.set_password('1234')
user49.save()
user49.user_organizations.add(org1)
print ' Created: ' + user49.username
user_email="jaquenetta.hot@evesch.com"
user50 = User(username='jaquenetta',email=user_email)
user50.first_name = 'Jaquenetta'
user50.last_name = 'Hot'
user50.is_superuser=False
user50.is_staff=False
user50.set_password('1234')
user50.save()
user50.user_organizations.add(org1)
print ' Created: ' + user50.username
user_email="jarah.hot@evesch.com"
user51 = User(username='jarah',email=user_email)
user51.first_name = 'Jarah'
user51.last_name = 'Hot'
user51.is_superuser=False
user51.is_staff=False
user51.set_password('1234')
user51.save()
user51.user_organizations.add(org1)
print ' Created: ' + user51.username
user_email="jardena.hot@evesch.com"
user52 = User(username='jardena',email=user_email)
user52.first_name = 'Jardena'
user52.last_name = 'Hot'
user52.is_superuser=False
user52.is_staff=False
user52.set_password('1234')
user52.save()
user52.user_organizations.add(org1)
print ' Created: ' + user52.username
user_email="jarita.hot@evesch.com"
user53 = User(username='jarita',email=user_email)
user53.first_name = 'Jarita'
user53.last_name = 'Hot'
user53.is_superuser=False
user53.is_staff=False
user53.set_password('1234')
user53.save()
user53.user_organizations.add(org1)
print ' Created: ' + user53.username
user_email="jarka.hot@evesch.com"
user54 = User(username='jarka',email=user_email)
user54.first_name = 'Jarka'
user54.last_name = 'Hot'
user54.is_superuser=False
user54.is_staff=False
user54.set_password('1234')
user54.save()
user54.user_organizations.add(org1)
print ' Created: ' + user54.username
user_email="jarmila.hot@evesch.com"
user55 = User(username='jarmila',email=user_email)
user55.first_name = 'Jarmila'
user55.last_name = 'Hot'
user55.is_superuser=False
user55.is_staff=False
user55.set_password('1234')
user55.save()
user55.user_organizations.add(org1)
print ' Created: ' + user55.username
user_email="jarrah.hot@evesch.com"
user56 = User(username='jarrah',email=user_email)
user56.first_name = 'Jarrah'
user56.last_name = 'Hot'
user56.is_superuser=False
user56.is_staff=False
user56.set_password('1234')
user56.save()
user56.user_organizations.add(org1)
print ' Created: ' + user56.username
user_email="jarvia.hot@evesch.com"
user57 = User(username='jarvia',email=user_email)
user57.first_name = 'Jarvia'
user57.last_name = 'Hot'
user57.is_superuser=False
user57.is_staff=False
user57.set_password('1234')
user57.save()
user57.user_organizations.add(org1)
print ' Created: ' + user57.username
user_email="jarvinia.hot@evesch.com"
user58 = User(username='jarvinia',email=user_email)
user58.first_name = 'Jarvinia'
user58.last_name = 'Hot'
user58.is_superuser=False
user58.is_staff=False
user58.set_password('1234')
user58.save()
user58.user_organizations.add(org1)
print ' Created: ' + user58.username
user_email="jasmine.hot@evesch.com"
user59 = User(username='jasmine',email=user_email)
user59.first_name = 'Jasmine'
user59.last_name = 'Hot'
user59.is_superuser=False
user59.is_staff=False
user59.set_password('1234')
user59.save()
user59.user_organizations.add(org1)
print ' Created: ' + user59.username
user_email="jaunie.hot@evesch.com"
user60 = User(username='jaunie',email=user_email)
user60.first_name = 'Jaunie'
user60.last_name = 'Hot'
user60.is_superuser=False
user60.is_staff=False
user60.set_password('1234')
user60.save()
user60.user_organizations.add(org1)
print ' Created: ' + user60.username
user_email="jaya.hot@evesch.com"
user61 = User(username='jaya',email=user_email)
user61.first_name = 'Jaya'
user61.last_name = 'Hot'
user61.is_superuser=False
user61.is_staff=False
user61.set_password('1234')
user61.save()
user61.user_organizations.add(org1)
print ' Created: ' + user61.username
user_email="jayani.hot@evesch.com"
user62 = User(username='jayani',email=user_email)
user62.first_name = 'Jayani'
user62.last_name = 'Hot'
user62.is_superuser=False
user62.is_staff=False
user62.set_password('1234')
user62.save()
user62.user_organizations.add(org1)
print ' Created: ' + user62.username
user_email="jayne.hot@evesch.com"
user63 = User(username='jayne',email=user_email)
user63.first_name = 'Jayne'
user63.last_name = 'Hot'
user63.is_superuser=False
user63.is_staff=False
user63.set_password('1234')
user63.save()
user63.user_organizations.add(org1)
print ' Created: ' + user63.username
user_email="jaythen.hot@evesch.com"
user64 = User(username='jaythen',email=user_email)
user64.first_name = 'Jaythen'
user64.last_name = 'Hot'
user64.is_superuser=False
user64.is_staff=False
user64.set_password('1234')
user64.save()
user64.user_organizations.add(org1)
print ' Created: ' + user64.username
user_email="jazlyn.hot@evesch.com"
user65 = User(username='jazlyn',email=user_email)
user65.first_name = 'Jazlyn'
user65.last_name = 'Hot'
user65.is_superuser=False
user65.is_staff=False
user65.set_password('1234')
user65.save()
user65.user_organizations.add(org1)
print ' Created: ' + user65.username
user_email="jean.hot@evesch.com"
user66 = User(username='jean',email=user_email)
user66.first_name = 'Jean'
user66.last_name = 'Hot'
user66.is_superuser=False
user66.is_staff=False
user66.set_password('1234')
user66.save()
user66.user_organizations.add(org1)
print ' Created: ' + user66.username
user_email="jeanne.hot@evesch.com"
user67 = User(username='jeanne',email=user_email)
user67.first_name = 'Jeanne'
user67.last_name = 'Hot'
user67.is_superuser=False
user67.is_staff=False
user67.set_password('1234')
user67.save()
user67.user_organizations.add(org1)
print ' Created: ' + user67.username
user_email="jeannette.hot@evesch.com"
user68 = User(username='jeannette',email=user_email)
user68.first_name = 'Jeannette'
user68.last_name = 'Hot'
user68.is_superuser=False
user68.is_staff=False
user68.set_password('1234')
user68.save()
user68.user_organizations.add(org1)
print ' Created: ' + user68.username
user_email="jehan.hot@evesch.com"
user69 = User(username='jehan',email=user_email)
user69.first_name = 'Jehan'
user69.last_name = 'Hot'
user69.is_superuser=False
user69.is_staff=False
user69.set_password('1234')
user69.save()
user69.user_organizations.add(org1)
print ' Created: ' + user69.username
user_email="jelena.hot@evesch.com"
user70 = User(username='jelena',email=user_email)
user70.first_name = 'Jelena'
user70.last_name = 'Hot'
user70.is_superuser=False
user70.is_staff=False
user70.set_password('1234')
user70.save()
user70.user_organizations.add(org1)
print ' Created: ' + user70.username
user_email="jemima.hot@evesch.com"
user71 = User(username='jemima',email=user_email)
user71.first_name = 'Jemima'
user71.last_name = 'Hot'
user71.is_superuser=False
user71.is_staff=False
user71.set_password('1234')
user71.save()
user71.user_organizations.add(org1)
print ' Created: ' + user71.username
user_email="jemma.hot@evesch.com"
user72 = User(username='jemma',email=user_email)
user72.first_name = 'Jemma'
user72.last_name = 'Hot'
user72.is_superuser=False
user72.is_staff=False
user72.set_password('1234')
user72.save()
user72.user_organizations.add(org1)
print ' Created: ' + user72.username
user_email="jena.hot@evesch.com"
user73 = User(username='jena',email=user_email)
user73.first_name = 'Jena'
user73.last_name = 'Hot'
user73.is_superuser=False
user73.is_staff=False
user73.set_password('1234')
user73.save()
user73.user_organizations.add(org1)
print ' Created: ' + user73.username
user_email="jenara.hot@evesch.com"
user74 = User(username='jenara',email=user_email)
user74.first_name = 'Jenara'
user74.last_name = 'Hot'
user74.is_superuser=False
user74.is_staff=False
user74.set_password('1234')
user74.save()
user74.user_organizations.add(org1)
print ' Created: ' + user74.username
user_email="jenay.hot@evesch.com"
user75 = User(username='jenay',email=user_email)
user75.first_name = 'Jenay'
user75.last_name = 'Hot'
user75.is_superuser=False
user75.is_staff=False
user75.set_password('1234')
user75.save()
user75.user_organizations.add(org1)
print ' Created: ' + user75.username
user_email="jendayi.hot@evesch.com"
user76 = User(username='jendayi',email=user_email)
user76.first_name = 'Jendayi'
user76.last_name = 'Hot'
user76.is_superuser=False
user76.is_staff=False
user76.set_password('1234')
user76.save()
user76.user_organizations.add(org1)
print ' Created: ' + user76.username
user_email="jendyose.hot@evesch.com"
user77 = User(username='jendyose',email=user_email)
user77.first_name = 'Jendyose'
user77.last_name = 'Hot'
user77.is_superuser=False
user77.is_staff=False
user77.set_password('1234')
user77.save()
user77.user_organizations.add(org1)
print ' Created: ' + user77.username
user_email="jenell.hot@evesch.com"
user78 = User(username='jenell',email=user_email)
user78.first_name = 'Jenell'
user78.last_name = 'Hot'
user78.is_superuser=False
user78.is_staff=False
user78.set_password('1234')
user78.save()
user78.user_organizations.add(org1)
print ' Created: ' + user78.username
user_email="jenica.hot@evesch.com"
user79 = User(username='jenica',email=user_email)
user79.first_name = 'Jenica'
user79.last_name = 'Hot'
user79.is_superuser=False
user79.is_staff=False
user79.set_password('1234')
user79.save()
user79.user_organizations.add(org1)
print ' Created: ' + user79.username
user_email="jenna.hot@evesch.com"
user80 = User(username='jenna',email=user_email)
user80.first_name = 'Jenna'
user80.last_name = 'Hot'
user80.is_superuser=False
user80.is_staff=False
user80.set_password('1234')
user80.save()
user80.user_organizations.add(org1)
print ' Created: ' + user80.username
user_email="jennifer.hot@evesch.com"
user81 = User(username='jennifer',email=user_email)
user81.first_name = 'Jennifer'
user81.last_name = 'Hot'
user81.is_superuser=False
user81.is_staff=False
user81.set_password('1234')
user81.save()
user81.user_organizations.add(org1)
print ' Created: ' + user81.username
user_email="jenny.hot@evesch.com"
user82 = User(username='jenny',email=user_email)
user82.first_name = 'Jenny'
user82.last_name = 'Hot'
user82.is_superuser=False
user82.is_staff=False
user82.set_password('1234')
user82.save()
user82.user_organizations.add(org1)
print ' Created: ' + user82.username
user_email="jeno.hot@evesch.com"
user83 = User(username='jeno',email=user_email)
user83.first_name = 'Jeno'
user83.last_name = 'Hot'
user83.is_superuser=False
user83.is_staff=False
user83.set_password('1234')
user83.save()
user83.user_organizations.add(org1)
print ' Created: ' + user83.username
user_email="jensine.hot@evesch.com"
user84 = User(username='jensine',email=user_email)
user84.first_name = 'Jensine'
user84.last_name = 'Hot'
user84.is_superuser=False
user84.is_staff=False
user84.set_password('1234')
user84.save()
user84.user_organizations.add(org1)
print ' Created: ' + user84.username
user_email="jeraldine.hot@evesch.com"
user85 = User(username='jeraldine',email=user_email)
user85.first_name = 'Jeraldine'
user85.last_name = 'Hot'
user85.is_superuser=False
user85.is_staff=False
user85.set_password('1234')
user85.save()
user85.user_organizations.add(org1)
print ' Created: ' + user85.username
user_email="jerarda.hot@evesch.com"
user86 = User(username='jerarda',email=user_email)
user86.first_name = 'Jerarda'
user86.last_name = 'Hot'
user86.is_superuser=False
user86.is_staff=False
user86.set_password('1234')
user86.save()
user86.user_organizations.add(org1)
print ' Created: ' + user86.username
user_email="jeremia.hot@evesch.com"
user87 = User(username='jeremia',email=user_email)
user87.first_name = 'Jeremia'
user87.last_name = 'Hot'
user87.is_superuser=False
user87.is_staff=False
user87.set_password('1234')
user87.save()
user87.user_organizations.add(org1)
print ' Created: ' + user87.username
user_email="jermain.hot@evesch.com"
user88 = User(username='jermain',email=user_email)
user88.first_name = 'Jermain'
user88.last_name = 'Hot'
user88.is_superuser=False
user88.is_staff=False
user88.set_password('1234')
user88.save()
user88.user_organizations.add(org1)
print ' Created: ' + user88.username
user_email="jermayne.hot@evesch.com"
user89 = User(username='jermayne',email=user_email)
user89.first_name = 'Jermayne'
user89.last_name = 'Hot'
user89.is_superuser=False
user89.is_staff=False
user89.set_password('1234')
user89.save()
user89.user_organizations.add(org1)
print ' Created: ' + user89.username
user_email="jerrica.hot@evesch.com"
user90 = User(username='jerrica',email=user_email)
user90.first_name = 'Jerrica'
user90.last_name = 'Hot'
user90.is_superuser=False
user90.is_staff=False
user90.set_password('1234')
user90.save()
user90.user_organizations.add(org1)
print ' Created: ' + user90.username
user_email="jerusha.hot@evesch.com"
user91 = User(username='jerusha',email=user_email)
user91.first_name = 'Jerusha'
user91.last_name = 'Hot'
user91.is_superuser=False
user91.is_staff=False
user91.set_password('1234')
user91.save()
user91.user_organizations.add(org1)
print ' Created: ' + user91.username
user_email="jesal.hot@evesch.com"
user92 = User(username='jesal',email=user_email)
user92.first_name = 'Jesal'
user92.last_name = 'Hot'
user92.is_superuser=False
user92.is_staff=False
user92.set_password('1234')
user92.save()
user92.user_organizations.add(org1)
print ' Created: ' + user92.username
user_email="jess.hot@evesch.com"
user93 = User(username='jess',email=user_email)
user93.first_name = 'Jess'
user93.last_name = 'Hot'
user93.is_superuser=False
user93.is_staff=False
user93.set_password('1234')
user93.save()
user93.user_organizations.add(org1)
print ' Created: ' + user93.username
user_email="jesse.hot@evesch.com"
user94 = User(username='jesse',email=user_email)
user94.first_name = 'Jesse'
user94.last_name = 'Hot'
user94.is_superuser=False
user94.is_staff=False
user94.set_password('1234')
user94.save()
user94.user_organizations.add(org1)
print ' Created: ' + user94.username
user_email="jessie.hot@evesch.com"
user95 = User(username='jessie',email=user_email)
user95.first_name = 'Jessie'
user95.last_name = 'Hot'
user95.is_superuser=False
user95.is_staff=False
user95.set_password('1234')
user95.save()
user95.user_organizations.add(org1)
print ' Created: ' + user95.username
user_email="jet.hot@evesch.com"
user96 = User(username='jet',email=user_email)
user96.first_name = 'Jet'
user96.last_name = 'Hot'
user96.is_superuser=False
user96.is_staff=False
user96.set_password('1234')
user96.save()
user96.user_organizations.add(org1)
print ' Created: ' + user96.username
user_email="jetta.hot@evesch.com"
user97 = User(username='jetta',email=user_email)
user97.first_name = 'Jetta'
user97.last_name = 'Hot'
user97.is_superuser=False
user97.is_staff=False
user97.set_password('1234')
user97.save()
user97.user_organizations.add(org1)
print ' Created: ' + user97.username
user_email="jewel.hot@evesch.com"
user98 = User(username='jewel',email=user_email)
user98.first_name = 'Jewel'
user98.last_name = 'Hot'
user98.is_superuser=False
user98.is_staff=False
user98.set_password('1234')
user98.save()
user98.user_organizations.add(org1)
print ' Created: ' + user98.username
user_email="jewell.hot@evesch.com"
user99 = User(username='jewell',email=user_email)
user99.first_name = 'Jewell'
user99.last_name = 'Hot'
user99.is_superuser=False
user99.is_staff=False
user99.set_password('1234')
user99.save()
user99.user_organizations.add(org1)
print ' Created: ' + user99.username
user_email="jezebel.hot@evesch.com"
user100 = User(username='jezebel',email=user_email)
user100.first_name = 'Jezebel'
user100.last_name = 'Hot'
user100.is_superuser=False
user100.is_staff=False
user100.set_password('1234')
user100.save()
user100.user_organizations.add(org1)
print ' Created: ' + user100.username
user_email="jezreel.hot@evesch.com"
user101 = User(username='jezreel',email=user_email)
user101.first_name = 'Jezreel'
user101.last_name = 'Hot'
user101.is_superuser=False
user101.is_staff=False
user101.set_password('1234')
user101.save()
user101.user_organizations.add(org1)
print ' Created: ' + user101.username
user_email="jiba.hot@evesch.com"
user102 = User(username='jiba',email=user_email)
user102.first_name = 'Jiba'
user102.last_name = 'Hot'
user102.is_superuser=False
user102.is_staff=False
user102.set_password('1234')
user102.save()
user102.user_organizations.add(org1)
print ' Created: ' + user102.username
user_email="jiera.hot@evesch.com"
user103 = User(username='jiera',email=user_email)
user103.first_name = 'Jiera'
user103.last_name = 'Hot'
user103.is_superuser=False
user103.is_staff=False
user103.set_password('1234')
user103.save()
user103.user_organizations.add(org1)
print ' Created: ' + user103.username
user_email="jigisha.hot@evesch.com"
user104 = User(username='jigisha',email=user_email)
user104.first_name = 'Jigisha'
user104.last_name = 'Hot'
user104.is_superuser=False
user104.is_staff=False
user104.set_password('1234')
user104.save()
user104.user_organizations.add(org1)
print ' Created: ' + user104.username
user_email="jihan.hot@evesch.com"
user105 = User(username='jihan',email=user_email)
user105.first_name = 'Jihan'
user105.last_name = 'Hot'
user105.is_superuser=False
user105.is_staff=False
user105.set_password('1234')
user105.save()
user105.user_organizations.add(org1)
print ' Created: ' + user105.username
user_email="jill.hot@evesch.com"
user106 = User(username='jill',email=user_email)
user106.first_name = 'Jill'
user106.last_name = 'Hot'
user106.is_superuser=False
user106.is_staff=False
user106.set_password('1234')
user106.save()
user106.user_organizations.add(org1)
print ' Created: ' + user106.username
user_email="jilli.hot@evesch.com"
user107 = User(username='jilli',email=user_email)
user107.first_name = 'Jilli'
user107.last_name = 'Hot'
user107.is_superuser=False
user107.is_staff=False
user107.set_password('1234')
user107.save()
user107.user_organizations.add(org1)
print ' Created: ' + user107.username
user_email="jillian.hot@evesch.com"
user108 = User(username='jillian',email=user_email)
user108.first_name = 'Jillian'
user108.last_name = 'Hot'
user108.is_superuser=False
user108.is_staff=False
user108.set_password('1234')
user108.save()
user108.user_organizations.add(org1)
print ' Created: ' + user108.username
user_email="jillie.hot@evesch.com"
user109 = User(username='jillie',email=user_email)
user109.first_name = 'Jillie'
user109.last_name = 'Hot'
user109.is_superuser=False
user109.is_staff=False
user109.set_password('1234')
user109.save()
user109.user_organizations.add(org1)
print ' Created: ' + user109.username
user_email="jilly.hot@evesch.com"
user110 = User(username='jilly',email=user_email)
user110.first_name = 'Jilly'
user110.last_name = 'Hot'
user110.is_superuser=False
user110.is_staff=False
user110.set_password('1234')
user110.save()
user110.user_organizations.add(org1)
print ' Created: ' + user110.username
user_email="jin.hot@evesch.com"
user111 = User(username='jin',email=user_email)
user111.first_name = 'Jin'
user111.last_name = 'Hot'
user111.is_superuser=False
user111.is_staff=False
user111.set_password('1234')
user111.save()
user111.user_organizations.add(org1)
print ' Created: ' + user111.username
user_email="jina.hot@evesch.com"
user112 = User(username='jina',email=user_email)
user112.first_name = 'Jina'
user112.last_name = 'Hot'
user112.is_superuser=False
user112.is_staff=False
user112.set_password('1234')
user112.save()
user112.user_organizations.add(org1)
print ' Created: ' + user112.username
user_email="jinx.hot@evesch.com"
user113 = User(username='jinx',email=user_email)
user113.first_name = 'Jinx'
user113.last_name = 'Hot'
user113.is_superuser=False
user113.is_staff=False
user113.set_password('1234')
user113.save()
user113.user_organizations.add(org1)
print ' Created: ' + user113.username
user_email="jirra.hot@evesch.com"
user114 = User(username='jirra',email=user_email)
user114.first_name = 'Jirra'
user114.last_name = 'Hot'
user114.is_superuser=False
user114.is_staff=False
user114.set_password('1234')
user114.save()
user114.user_organizations.add(org1)
print ' Created: ' + user114.username
user_email="joakima.hot@evesch.com"
user115 = User(username='joakima',email=user_email)
user115.first_name = 'Joakima'
user115.last_name = 'Hot'
user115.is_superuser=False
user115.is_staff=False
user115.set_password('1234')
user115.save()
user115.user_organizations.add(org1)
print ' Created: ' + user115.username
user_email="joan.hot@evesch.com"
user116 = User(username='joan',email=user_email)
user116.first_name = 'Joan'
user116.last_name = 'Hot'
user116.is_superuser=False
user116.is_staff=False
user116.set_password('1234')
user116.save()
user116.user_organizations.add(org1)
print ' Created: ' + user116.username
user_email="joann.hot@evesch.com"
user117 = User(username='joann',email=user_email)
user117.first_name = 'Joann'
user117.last_name = 'Hot'
user117.is_superuser=False
user117.is_staff=False
user117.set_password('1234')
user117.save()
user117.user_organizations.add(org1)
print ' Created: ' + user117.username
user_email="joanna.hot@evesch.com"
user118 = User(username='joanna',email=user_email)
user118.first_name = 'Joanna'
user118.last_name = 'Hot'
user118.is_superuser=False
user118.is_staff=False
user118.set_password('1234')
user118.save()
user118.user_organizations.add(org1)
print ' Created: ' + user118.username
user_email="joanne.hot@evesch.com"
user119 = User(username='joanne',email=user_email)
user119.first_name = 'Joanne'
user119.last_name = 'Hot'
user119.is_superuser=False
user119.is_staff=False
user119.set_password('1234')
user119.save()
user119.user_organizations.add(org1)
print ' Created: ' + user119.username
user_email="jobey.hot@evesch.com"
user120 = User(username='jobey',email=user_email)
user120.first_name = 'Jobey'
user120.last_name = 'Hot'
user120.is_superuser=False
user120.is_staff=False
user120.set_password('1234')
user120.save()
user120.user_organizations.add(org1)
print ' Created: ' + user120.username
user_email="jobina.hot@evesch.com"
user121 = User(username='jobina',email=user_email)
user121.first_name = 'Jobina'
user121.last_name = 'Hot'
user121.is_superuser=False
user121.is_staff=False
user121.set_password('1234')
user121.save()
user121.user_organizations.add(org1)
print ' Created: ' + user121.username
user_email="jocasta.hot@evesch.com"
user122 = User(username='jocasta',email=user_email)
user122.first_name = 'Jocasta'
user122.last_name = 'Hot'
user122.is_superuser=False
user122.is_staff=False
user122.set_password('1234')
user122.save()
user122.user_organizations.add(org1)
print ' Created: ' + user122.username
user_email="jocelyn.hot@evesch.com"
user123 = User(username='jocelyn',email=user_email)
user123.first_name = 'Jocelyn'
user123.last_name = 'Hot'
user123.is_superuser=False
user123.is_staff=False
user123.set_password('1234')
user123.save()
user123.user_organizations.add(org1)
print ' Created: ' + user123.username
user_email="jocosa.hot@evesch.com"
user124 = User(username='jocosa',email=user_email)
user124.first_name = 'Jocosa'
user124.last_name = 'Hot'
user124.is_superuser=False
user124.is_staff=False
user124.set_password('1234')
user124.save()
user124.user_organizations.add(org1)
print ' Created: ' + user124.username
user_email="jocunda.hot@evesch.com"
user125 = User(username='jocunda',email=user_email)
user125.first_name = 'Jocunda'
user125.last_name = 'Hot'
user125.is_superuser=False
user125.is_staff=False
user125.set_password('1234')
user125.save()
user125.user_organizations.add(org1)
print ' Created: ' + user125.username
user_email="jodi.hot@evesch.com"
user126 = User(username='jodi',email=user_email)
user126.first_name = 'Jodi'
user126.last_name = 'Hot'
user126.is_superuser=False
user126.is_staff=False
user126.set_password('1234')
user126.save()
user126.user_organizations.add(org1)
print ' Created: ' + user126.username
user_email="jodie.hot@evesch.com"
user127 = User(username='jodie',email=user_email)
user127.first_name = 'Jodie'
user127.last_name = 'Hot'
user127.is_superuser=False
user127.is_staff=False
user127.set_password('1234')
user127.save()
user127.user_organizations.add(org1)
print ' Created: ' + user127.username
user_email="joelle.hot@evesch.com"
user128 = User(username='joelle',email=user_email)
user128.first_name = 'Joelle'
user128.last_name = 'Hot'
user128.is_superuser=False
user128.is_staff=False
user128.set_password('1234')
user128.save()
user128.user_organizations.add(org1)
print ' Created: ' + user128.username
user_email="joelliane.hot@evesch.com"
user129 = User(username='joelliane',email=user_email)
user129.first_name = 'Joelliane'
user129.last_name = 'Hot'
user129.is_superuser=False
user129.is_staff=False
user129.set_password('1234')
user129.save()
user129.user_organizations.add(org1)
print ' Created: ' + user129.username
user_email="joesa.hot@evesch.com"
user130 = User(username='joesa',email=user_email)
user130.first_name = 'Joesa'
user130.last_name = 'Hot'
user130.is_superuser=False
user130.is_staff=False
user130.set_password('1234')
user130.save()
user130.user_organizations.add(org1)
print ' Created: ' + user130.username
user_email="johanna.hot@evesch.com"
user131 = User(username='johanna',email=user_email)
user131.first_name = 'Johanna'
user131.last_name = 'Hot'
user131.is_superuser=False
user131.is_staff=False
user131.set_password('1234')
user131.save()
user131.user_organizations.add(org1)
print ' Created: ' + user131.username
user_email="jolan.hot@evesch.com"
user132 = User(username='jolan',email=user_email)
user132.first_name = 'Jolan'
user132.last_name = 'Hot'
user132.is_superuser=False
user132.is_staff=False
user132.set_password('1234')
user132.save()
user132.user_organizations.add(org1)
print ' Created: ' + user132.username
user_email="jolanda.hot@evesch.com"
user133 = User(username='jolanda',email=user_email)
user133.first_name = 'Jolanda'
user133.last_name = 'Hot'
user133.is_superuser=False
user133.is_staff=False
user133.set_password('1234')
user133.save()
user133.user_organizations.add(org1)
print ' Created: ' + user133.username
user_email="jolanta.hot@evesch.com"
user134 = User(username='jolanta',email=user_email)
user134.first_name = 'Jolanta'
user134.last_name = 'Hot'
user134.is_superuser=False
user134.is_staff=False
user134.set_password('1234')
user134.save()
user134.user_organizations.add(org1)
print ' Created: ' + user134.username
user_email="jolene.hot@evesch.com"
user135 = User(username='jolene',email=user_email)
user135.first_name = 'Jolene'
user135.last_name = 'Hot'
user135.is_superuser=False
user135.is_staff=False
user135.set_password('1234')
user135.save()
user135.user_organizations.add(org1)
print ' Created: ' + user135.username
user_email="jolie.hot@evesch.com"
user136 = User(username='jolie',email=user_email)
user136.first_name = 'Jolie'
user136.last_name = 'Hot'
user136.is_superuser=False
user136.is_staff=False
user136.set_password('1234')
user136.save()
user136.user_organizations.add(org1)
print ' Created: ' + user136.username
user_email="jonesy.hot@evesch.com"
user137 = User(username='jonesy',email=user_email)
user137.first_name = 'Jonesy'
user137.last_name = 'Hot'
user137.is_superuser=False
user137.is_staff=False
user137.set_password('1234')
user137.save()
user137.user_organizations.add(org1)
print ' Created: ' + user137.username
user_email="joni.hot@evesch.com"
user138 = User(username='joni',email=user_email)
user138.first_name = 'Joni'
user138.last_name = 'Hot'
user138.is_superuser=False
user138.is_staff=False
user138.set_password('1234')
user138.save()
user138.user_organizations.add(org1)
print ' Created: ' + user138.username
user_email="jonie.hot@evesch.com"
user139 = User(username='jonie',email=user_email)
user139.first_name = 'Jonie'
user139.last_name = 'Hot'
user139.is_superuser=False
user139.is_staff=False
user139.set_password('1234')
user139.save()
user139.user_organizations.add(org1)
print ' Created: ' + user139.username
user_email="jonina.hot@evesch.com"
user140 = User(username='jonina',email=user_email)
user140.first_name = 'Jonina'
user140.last_name = 'Hot'
user140.is_superuser=False
user140.is_staff=False
user140.set_password('1234')
user140.save()
user140.user_organizations.add(org1)
print ' Created: ' + user140.username
user_email="jonquil.hot@evesch.com"
user141 = User(username='jonquil',email=user_email)
user141.first_name = 'Jonquil'
user141.last_name = 'Hot'
user141.is_superuser=False
user141.is_staff=False
user141.set_password('1234')
user141.save()
user141.user_organizations.add(org1)
print ' Created: ' + user141.username
user_email="jooeun.hot@evesch.com"
user142 = User(username='jooeun',email=user_email)
user142.first_name = 'JooEun'
user142.last_name = 'Hot'
user142.is_superuser=False
user142.is_staff=False
user142.set_password('1234')
user142.save()
user142.user_organizations.add(org1)
print ' Created: ' + user142.username
user_email="jora.hot@evesch.com"
user143 = User(username='jora',email=user_email)
user143.first_name = 'Jora'
user143.last_name = 'Hot'
user143.is_superuser=False
user143.is_staff=False
user143.set_password('1234')
user143.save()
user143.user_organizations.add(org1)
print ' Created: ' + user143.username
user_email="jordan.hot@evesch.com"
user144 = User(username='jordan',email=user_email)
user144.first_name = 'Jordan'
user144.last_name = 'Hot'
user144.is_superuser=False
user144.is_staff=False
user144.set_password('1234')
user144.save()
user144.user_organizations.add(org1)
print ' Created: ' + user144.username
user_email="jordana.hot@evesch.com"
user145 = User(username='jordana',email=user_email)
user145.first_name = 'Jordana'
user145.last_name = 'Hot'
user145.is_superuser=False
user145.is_staff=False
user145.set_password('1234')
user145.save()
user145.user_organizations.add(org1)
print ' Created: ' + user145.username
user_email="jordane.hot@evesch.com"
user146 = User(username='jordane',email=user_email)
user146.first_name = 'Jordane'
user146.last_name = 'Hot'
user146.is_superuser=False
user146.is_staff=False
user146.set_password('1234')
user146.save()
user146.user_organizations.add(org1)
print ' Created: ' + user146.username
user_email="joscelin.hot@evesch.com"
user147 = User(username='joscelin',email=user_email)
user147.first_name = 'Joscelin'
user147.last_name = 'Hot'
user147.is_superuser=False
user147.is_staff=False
user147.set_password('1234')
user147.save()
user147.user_organizations.add(org1)
print ' Created: ' + user147.username
user_email="josephine.hot@evesch.com"
user148 = User(username='josephine',email=user_email)
user148.first_name = 'Josephine'
user148.last_name = 'Hot'
user148.is_superuser=False
user148.is_staff=False
user148.set_password('1234')
user148.save()
user148.user_organizations.add(org1)
print ' Created: ' + user148.username
user_email="josie.hot@evesch.com"
user149 = User(username='josie',email=user_email)
user149.first_name = 'Josie'
user149.last_name = 'Hot'
user149.is_superuser=False
user149.is_staff=False
user149.set_password('1234')
user149.save()
user149.user_organizations.add(org1)
print ' Created: ' + user149.username
user_email="joslin.hot@evesch.com"
user150 = User(username='joslin',email=user_email)
user150.first_name = 'Joslin'
user150.last_name = 'Hot'
user150.is_superuser=False
user150.is_staff=False
user150.set_password('1234')
user150.save()
user150.user_organizations.add(org1)
print ' Created: ' + user150.username
user_email="josslyn.hot@evesch.com"
user151 = User(username='josslyn',email=user_email)
user151.first_name = 'Josslyn'
user151.last_name = 'Hot'
user151.is_superuser=False
user151.is_staff=False
user151.set_password('1234')
user151.save()
user151.user_organizations.add(org1)
print ' Created: ' + user151.username
user_email="jovita.hot@evesch.com"
user152 = User(username='jovita',email=user_email)
user152.first_name = 'Jovita'
user152.last_name = 'Hot'
user152.is_superuser=False
user152.is_staff=False
user152.set_password('1234')
user152.save()
user152.user_organizations.add(org1)
print ' Created: ' + user152.username
user_email="joy.hot@evesch.com"
user153 = User(username='joy',email=user_email)
user153.first_name = 'Joy'
user153.last_name = 'Hot'
user153.is_superuser=False
user153.is_staff=False
user153.set_password('1234')
user153.save()
user153.user_organizations.add(org1)
print ' Created: ' + user153.username
user_email="joyanne.hot@evesch.com"
user154 = User(username='joyanne',email=user_email)
user154.first_name = 'Joyanne'
user154.last_name = 'Hot'
user154.is_superuser=False
user154.is_staff=False
user154.set_password('1234')
user154.save()
user154.user_organizations.add(org1)
print ' Created: ' + user154.username
user_email="joyce.hot@evesch.com"
user155 = User(username='joyce',email=user_email)
user155.first_name = 'Joyce'
user155.last_name = 'Hot'
user155.is_superuser=False
user155.is_staff=False
user155.set_password('1234')
user155.save()
user155.user_organizations.add(org1)
print ' Created: ' + user155.username
user_email="juana.hot@evesch.com"
user156 = User(username='juana',email=user_email)
user156.first_name = 'Juana'
user156.last_name = 'Hot'
user156.is_superuser=False
user156.is_staff=False
user156.set_password('1234')
user156.save()
user156.user_organizations.add(org1)
print ' Created: ' + user156.username
user_email="juanita.hot@evesch.com"
user157 = User(username='juanita',email=user_email)
user157.first_name = 'Juanita'
user157.last_name = 'Hot'
user157.is_superuser=False
user157.is_staff=False
user157.set_password('1234')
user157.save()
user157.user_organizations.add(org1)
print ' Created: ' + user157.username
user_email="judith.hot@evesch.com"
user158 = User(username='judith',email=user_email)
user158.first_name = 'Judith'
user158.last_name = 'Hot'
user158.is_superuser=False
user158.is_staff=False
user158.set_password('1234')
user158.save()
user158.user_organizations.add(org1)
print ' Created: ' + user158.username
user_email="judy.hot@evesch.com"
user159 = User(username='judy',email=user_email)
user159.first_name = 'Judy'
user159.last_name = 'Hot'
user159.is_superuser=False
user159.is_staff=False
user159.set_password('1234')
user159.save()
user159.user_organizations.add(org1)
print ' Created: ' + user159.username
user_email="juene.hot@evesch.com"
user160 = User(username='juene',email=user_email)
user160.first_name = 'Juene'
user160.last_name = 'Hot'
user160.is_superuser=False
user160.is_staff=False
user160.set_password('1234')
user160.save()
user160.user_organizations.add(org1)
print ' Created: ' + user160.username
user_email="juhi.hot@evesch.com"
user161 = User(username='juhi',email=user_email)
user161.first_name = 'Juhi'
user161.last_name = 'Hot'
user161.is_superuser=False
user161.is_staff=False
user161.set_password('1234')
user161.save()
user161.user_organizations.add(org1)
print ' Created: ' + user161.username
user_email="jules.hot@evesch.com"
user162 = User(username='jules',email=user_email)
user162.first_name = 'Jules'
user162.last_name = 'Hot'
user162.is_superuser=False
user162.is_staff=False
user162.set_password('1234')
user162.save()
user162.user_organizations.add(org1)
print ' Created: ' + user162.username
user_email="julia.hot@evesch.com"
user163 = User(username='julia',email=user_email)
user163.first_name = 'Julia'
user163.last_name = 'Hot'
user163.is_superuser=False
user163.is_staff=False
user163.set_password('1234')
user163.save()
user163.user_organizations.add(org1)
print ' Created: ' + user163.username
user_email="juliana.hot@evesch.com"
user164 = User(username='juliana',email=user_email)
user164.first_name = 'Juliana'
user164.last_name = 'Hot'
user164.is_superuser=False
user164.is_staff=False
user164.set_password('1234')
user164.save()
user164.user_organizations.add(org1)
print ' Created: ' + user164.username
user_email="julianna.hot@evesch.com"
user165 = User(username='julianna',email=user_email)
user165.first_name = 'Julianna'
user165.last_name = 'Hot'
user165.is_superuser=False
user165.is_staff=False
user165.set_password('1234')
user165.save()
user165.user_organizations.add(org1)
print ' Created: ' + user165.username
user_email="julianne.hot@evesch.com"
user166 = User(username='julianne',email=user_email)
user166.first_name = 'Julianne'
user166.last_name = 'Hot'
user166.is_superuser=False
user166.is_staff=False
user166.set_password('1234')
user166.save()
user166.user_organizations.add(org1)
print ' Created: ' + user166.username
user_email="julie.hot@evesch.com"
user167 = User(username='julie',email=user_email)
user167.first_name = 'Julie'
user167.last_name = 'Hot'
user167.is_superuser=False
user167.is_staff=False
user167.set_password('1234')
user167.save()
user167.user_organizations.add(org1)
print ' Created: ' + user167.username
user_email="juliet.hot@evesch.com"
user168 = User(username='juliet',email=user_email)
user168.first_name = 'Juliet'
user168.last_name = 'Hot'
user168.is_superuser=False
user168.is_staff=False
user168.set_password('1234')
user168.save()
user168.user_organizations.add(org1)
print ' Created: ' + user168.username
user_email="julinka.hot@evesch.com"
user169 = User(username='julinka',email=user_email)
user169.first_name = 'Julinka'
user169.last_name = 'Hot'
user169.is_superuser=False
user169.is_staff=False
user169.set_password('1234')
user169.save()
user169.user_organizations.add(org1)
print ' Created: ' + user169.username
user_email="julya.hot@evesch.com"
user170 = User(username='julya',email=user_email)
user170.first_name = 'Julya'
user170.last_name = 'Hot'
user170.is_superuser=False
user170.is_staff=False
user170.set_password('1234')
user170.save()
user170.user_organizations.add(org1)
print ' Created: ' + user170.username
user_email="jumoke.hot@evesch.com"
user171 = User(username='jumoke',email=user_email)
user171.first_name = 'Jumoke'
user171.last_name = 'Hot'
user171.is_superuser=False
user171.is_staff=False
user171.set_password('1234')
user171.save()
user171.user_organizations.add(org1)
print ' Created: ' + user171.username
user_email="jun.hot@evesch.com"
user172 = User(username='jun',email=user_email)
user172.first_name = 'Jun'
user172.last_name = 'Hot'
user172.is_superuser=False
user172.is_staff=False
user172.set_password('1234')
user172.save()
user172.user_organizations.add(org1)
print ' Created: ' + user172.username
user_email="june.hot@evesch.com"
user173 = User(username='june',email=user_email)
user173.first_name = 'June'
user173.last_name = 'Hot'
user173.is_superuser=False
user173.is_staff=False
user173.set_password('1234')
user173.save()
user173.user_organizations.add(org1)
print ' Created: ' + user173.username
user_email="juniper.hot@evesch.com"
user174 = User(username='juniper',email=user_email)
user174.first_name = 'Juniper'
user174.last_name = 'Hot'
user174.is_superuser=False
user174.is_staff=False
user174.set_password('1234')
user174.save()
user174.user_organizations.add(org1)
print ' Created: ' + user174.username
user_email="juno.hot@evesch.com"
user175 = User(username='juno',email=user_email)
user175.first_name = 'Juno'
user175.last_name = 'Hot'
user175.is_superuser=False
user175.is_staff=False
user175.set_password('1234')
user175.save()
user175.user_organizations.add(org1)
print ' Created: ' + user175.username
user_email="justine.hot@evesch.com"
user176 = User(username='justine',email=user_email)
user176.first_name = 'Justine'
user176.last_name = 'Hot'
user176.is_superuser=False
user176.is_staff=False
user176.set_password('1234')
user176.save()
user176.user_organizations.add(org1)
print ' Created: ' + user176.username
user_email="jutta.hot@evesch.com"
user177 = User(username='jutta',email=user_email)
user177.first_name = 'Jutta'
user177.last_name = 'Hot'
user177.is_superuser=False
user177.is_staff=False
user177.set_password('1234')
user177.save()
user177.user_organizations.add(org1)
print ' Created: ' + user177.username
user_email="jutte.hot@evesch.com"
user178 = User(username='jutte',email=user_email)
user178.first_name = 'Jutte'
user178.last_name = 'Hot'
user178.is_superuser=False
user178.is_staff=False
user178.set_password('1234')
user178.save()
user178.user_organizations.add(org1)
print ' Created: ' + user178.username
user_email="jyoti.hot@evesch.com"
user179 = User(username='jyoti',email=user_email)
user179.first_name = 'Jyoti'
user179.last_name = 'Hot'
user179.is_superuser=False
user179.is_staff=False
user179.set_password('1234')
user179.save()
user179.user_organizations.add(org1)
print ' Created: ' + user179.username
user_email="jyotsna.hot@evesch.com"
user180 = User(username='jyotsna',email=user_email)
user180.first_name = 'Jyotsna'
user180.last_name = 'Hot'
user180.is_superuser=False
user180.is_staff=False
user180.set_password('1234')
user180.save()
user180.user_organizations.add(org1)
print ' Created: ' + user180.username

## Create some groups
print "Creating Groups" 
UserGroup.objects.init_org_groups(org1, user1)
g1 = UserGroup.objects.all()[0]
user2.user_groups.add(g1)
user0.user_groups.add(g1)
UserGroup.objects.init_org_groups(org2, user2)
UserGroup.objects.init_org_groups(org3, user2)
UserGroup.objects.init_org_groups(org4, user2)
UserGroup.objects.init_org_groups(org5, user2)

## Create some events
print "Creating Events" 
event1 = Event.objects.create_event("IWU Event 1",user1,org1,event_type1,datetime(2009,07,25,12,00,00))
event1.event_desc = "This is event 1"
event1.save()
print " Created: " + event1.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name

event2 = Event.objects.create_event("IWU Event 2",user2,org1,event_type1,datetime(2009,07,14,12,00,00))
event2.event_desc = "This is event 2"
event2.save()
print " Created: " + event2.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name

event3 = Event.objects.create_event("IWU Event 3",user2,org1,event_type1,datetime(2009,8,14,12,00,00))
event3.event_desc = "This is event 3"
event3.save()
print " Created: " + event3.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name

event4 = Event.objects.create_event("IWU Event 4",user2,org1,event_type1,datetime(2009,9,14,12,00,00))
event4.event_desc = "This is event 4"
event4.save()
print " Created: " + event4.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name

event5 = Event.objects.create_event("IWU Event 5",user1,org1,event_type1,datetime(2009,9,14,12,00,00))
event5.event_desc = "This is event 5"
event5.save()
print " Created: " + event5.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name

event6 = Event.objects.create_event("IWU Event 6",user2,org1,event_type1,datetime(2009,9,14,12,00,00))
event6.event_desc = "This is event 6"
event6.save()
print " Created: " + event6.event_name + " of type " + event_type1.type_name + " in org " + org1.org_short_name

