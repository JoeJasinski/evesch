from icalendar import Calendar, vCalAddress, vText
import icalendar
from datetime import timedelta
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.syndication.views import feed
from django.utils import feedgenerator
from django.template.loader import render_to_string
from django.http import HttpResponse
from evesch.org.models import Organization
from evesch.event.models import Event
from evesch.core.feed.feeds import OrgFeed
from evesch.euser.models import eUser, get_current_user


def org_rss(request,org_short_name,org_feed_hash):
    try: 
        """
        """
        host = request.META['HTTP_HOST']
        current_org, message = Organization.objects.get_current_org(org_short_name)
        if message:
            return HttpResponseRedirect(reverse('org_orgs_list'))
        
        if not org_feed_hash == current_org.org_feed_hash:
            return HttpResponseRedirect(reverse('org_org_view', kwargs={'org_short_name':current_org.org_short_name}))
        
        events = current_org.event_set.all().order_by('-event_date')
        orgfeed = feedgenerator.Rss201rev2Feed(title=current_org.org_name, 
           link="http://%s%s" % (host, reverse('event_events_list',kwargs={'org_short_name':current_org.org_short_name,})), 
           description=current_org.org_desc, language='en', 
           )
        
        for event in events:
            orgfeed.add_item(
            title=event.event_name, 
            link="http://%s%s" % (host, reverse('event_event_view', kwargs={'org_short_name':current_org.org_short_name,'event_hash':event.event_hash})), 
            description="Event on: %s --  Description: %s" % (event.event_date.strftime('%d %b %Y'), event.event_desc),
            categories=(event.event_type,),
            author_name=event.event_creator_name,
            pubdate=event.event_created_date)
        
        response = HttpResponse()
        response['Content-Type'] = 'application/rss+xml'
        response.write(orgfeed.writeString('UTF-8'))
        #template_name = "error.html"
        return response
    except ObjectDoesNotExist:
        context = {'error':"Organization does not exist",}
        template_name = "error.html"
    return render_to_response(template_name,context,context_instance=RequestContext(request))

def org_ics(request,org_short_name,org_feed_hash):
    host = request.META['HTTP_HOST']
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if message:
        return HttpResponseRedirect(reverse('org_orgs_list'))
 
    if not org_feed_hash == current_org.org_feed_hash:
        return HttpResponseRedirect(reverse('org_org_view', kwargs={'org_short_name':current_org.org_short_name}))
    
    events = current_org.event_set.all().order_by('-event_date')
    orgical = Calendar()

    orgical['summary'] = "Calendar for organization %s" % (current_org.org_name)
    orgical.add('prodid', '-//Evesch//NONSGML v1.0//EN')
    orgical.add('version', '2.0')

    for event in events:
        cal_event = icalendar.Event()
        cal_event.add('summary', event.event_name)
        cal_event.add('dtstart', event.event_date)
        cal_event.add('description', event.event_desc)
        cal_event.add('categories',event.event_type)
        cal_event.add('duration',timedelta(hours=1))
        cal_event.add('url',"http://%s%s" % (host,  reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':event.event_hash,})))
        if event.event_creator_name.email:
            organizer_n = event.event_creator_name.email
        else:
            organizer_n = "%s %s" % (event.event_creator_name.first_name, event.event_creator_name.last_name)
        organizer = vCalAddress('MAILTO:' + organizer_n)
        organizer.params['cn'] = vText("%s %s" % (event.event_creator_name.first_name, event.event_creator_name.last_name))
        organizer.params['role'] = vText('CREATOR')
        cal_event.add('organizer', organizer, encode=0)
        orgical.add_component(cal_event)

    template_name = "core/message.html"
    context = {}
    
    response = HttpResponse()
    response['Content-Type'] = 'text/calendar'
    response.write(orgical.as_string())
    #template_name = "error.html"
    return response
    

def user_rss(request,username,user_feed_hash):
    try: 
        """        """
        host = request.META['HTTP_HOST']
        current_user, message = get_current_user(username)
        if message:
            return HttpResponseRedirect(reverse('home'))
        
        if not user_feed_hash == current_user.user_feed_hash:
            return HttpResponseRedirect(reverse('euser_user_view', kwargs={'username':current_user.username}))
        
        user_events = Event.objects.filter(attendee__in=current_user.attendee_set.all()).order_by('-event_date')
        orgfeed = feedgenerator.Rss201rev2Feed(title=current_user.username, 
           link="http://%s%s" % (host, reverse('euser_user_view', kwargs={'username':current_user.username}))  , 
           description=current_user.about, language='en', 
           )
        
        for event in user_events:
            orgfeed.add_item(
            title=event.event_name, 
            link="http://%s%s" % (host,  reverse('event_event_view', kwargs={'org_short_name':event.event_org.org_short_name,'event_hash':event.event_hash})), 
            description="Event on: %s --  Description: %s" % (event.event_date.strftime('%d %b %Y'), event.event_desc),
            categories=(event.event_type,),
            author_name=event.event_creator_name,
            pubdate=event.event_created_date)
        
        response = HttpResponse()
        response['Content-Type'] = 'application/rss+xml'
        response.write(orgfeed.writeString('UTF-8'))
        #template_name = "error.html"
        return response
    except ObjectDoesNotExist:
        context = {'error':"Organization does not exist",}
        template_name = "error.html"
    return render_to_response(template_name,context,context_instance=RequestContext(request))


def user_ics(request,username,user_feed_hash):
    host = request.META['HTTP_HOST']
    current_user, message = get_current_user(username)
    if message:
        return HttpResponseRedirect(reverse('home'))

    #user_events = Event.objects.all()
    if not user_feed_hash == current_user.user_feed_hash:
        return HttpResponseRedirect(reverse('euser_user_view', kwargs={'username':current_user.username}))
    
    user_events =  Event.objects.filter(attendee__in=current_user.attendee_set.all()).order_by('-event_date')
    userical = Calendar()

    userical['summary'] = "Calendar for user %s" % (current_user.username)
    userical.add('prodid', '-//Evesch//NONSGML v1.0//EN')
    userical.add('version', '2.0')

    for event in user_events:
        cal_event = icalendar.Event()
        cal_event.add('summary', event.event_name)
        cal_event.add('dtstart', event.event_date)
        cal_event.add('description', event.event_desc)
        cal_event.add('categories',event.event_type)
        cal_event.add('duration',timedelta(hours=1))
        cal_event.add('url',"http://" + host + reverse('event_event_view',kwargs={'org_short_name':event.event_org.org_short_name,'event_hash':event.event_hash,}))
        if event.event_creator_name.email:
            organizer_n = event.event_creator_name.email
        else:
            organizer_n = "%s %s" % (event.event_creator_name.first_name, event.event_creator_name.last_name)
        organizer = vCalAddress('MAILTO:' + organizer_n)
        organizer.params['cn'] = vText("%s %s" % (event.event_creator_name.first_name, event.event_creator_name.last_name))
        organizer.params['role'] = vText('CREATOR')
        cal_event.add('organizer', organizer, encode=0)
        userical.add_component(cal_event)

    template_name = "core/message.html"
    context = {}
    
    response = HttpResponse()
    response['Content-Type'] = 'text/calendar'
    response.write(userical.as_string())
    #template_name = "error.html"
    return response
    