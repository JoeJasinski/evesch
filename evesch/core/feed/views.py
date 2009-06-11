# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from org.models import Organization
from event.models import Event
from core.feed.feeds import OrgFeed
from django.contrib.syndication.views import feed
from django.utils import feedgenerator
from django.template.loader import render_to_string
from django.http import HttpResponse
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import timedelta

def org_rss(request,org_short_name,org_feed_hash):
    try: 
        """
        feeds = { 'org_feed': OrgFeed, }
        current_org = Organization.objects.get(org_short_name=org_short_name,org_active=True)
        context = {'error':"RSS Not implemented",}
        #raise AssertionError
        orgfeed = feed(request, reverse('core_feed_org_rss',
                                        kwargs={'org_short_name':current_org.org_short_name,
                                                'org_feed_hash':org_feed_hash,}
                                        ),feeds)
        """
        host = request.META['HTTP_HOST']
        current_org = Organization.objects.get(org_short_name=org_short_name,org_active=True)
        events = current_org.event_set.all().order_by('-event_date')
        orgfeed = feedgenerator.Rss201rev2Feed(title=current_org.org_name, 
           link="http://" + host + reverse('event_events_list',kwargs={'org_short_name':current_org.org_short_name,}), 
           description=current_org.org_desc, language='en', 
           )
        
        for event in events:
            orgfeed.add_item(
            title=event.event_name, 
            link="http://" + host + reverse('event_event_view', kwargs={'org_short_name':current_org.org_short_name,'event_hash':event.event_hash}), 
            description="Event on: " + event.event_date.strftime('%d %b %Y') + " --  Description: " + event.event_desc,
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
    current_org = Organization.objects.get(org_short_name=org_short_name,org_active=True)
    events = current_org.event_set.all().order_by('-event_date')
    orgical = Calendar()

    orgical['summary'] = "Calendar for organization " + current_org.org_name
    orgical.add('prodid', '-//Evesch//NONSGML v1.0//EN')
    orgical.add('version', '2.0')


    for event in events:
        cal_event = Event()
        cal_event.add('summary', event.event_name)
        cal_event.add('dtstart', event.event_date)
        cal_event.add('description', event.event_desc)
        cal_event.add('categories',event.event_type)
        cal_event.add('duration',timedelta(hours=1))
        cal_event.add('url',"http://" + host + reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':event.event_hash,}))
        if event.event_creator_name.email:
            organizer_n = event.event_creator_name.email
        else:
            organizer_n = event.event_creator_name.first_name + " " + event.event_creator_name.last_name
        organizer = vCalAddress('MAILTO:' + organizer_n)
        organizer.params['cn'] = vText(event.event_creator_name.first_name + " " + event.event_creator_name.last_name)
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
    