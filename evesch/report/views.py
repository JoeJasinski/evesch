# Create your views here.
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.lib import Message
from euser.models import User, get_current_user
from org.models import Organization
from django.contrib.auth.decorators import login_required
from event.models import EventType
from report.forms import ReportFilterForm
from datetime import datetime

@login_required
def org_reports(request,org_short_name, type='generic', template_name=None):
    min_event_date = datetime.date
    max_event_date = datetime.date
    if request.method == 'POST': 
        form = ReportFilterForm(initial=request.POST)
        if form.is_valid():
            min_event_date = form.cleaned_data['min_event_date']
            max_event_date = form.cleaned_data['max_event_date']
        raise AssertionError(str(min_event_date) + " " + str(max_event_date) )
    else:
        form = ReportFilterForm()
    
    class OrgWrapper(object):
        def __init__(self):
            eventtypes = []
            users = []
            
    class EventTypeWrapper(object):
        def __init__(self):
            eventtype = None
            events = []
    
    class UserWrapper(object):
        def __init__(self):
            user = None
            events = []
            attending = []
            
    org_w = None
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:    
        current_user, message = get_current_user(request.user)
    if not message:    
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Add Event"), text=_("You cannot add an event in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        
        if type == 'user':
            type_display = _("Report grouped by User")
            org_w = OrgWrapper()
            org_w.users = []
            for user in current_users.get_member():
                user_w = UserWrapper()
                user_w.user = user
                
                # needs more code here
            
            
        elif type == 'eventtype':            
            type_display = _("Report grouped by Event Type")
            org_w = OrgWrapper()
            org_w.eventtypes = []
            for event_type in current_org.get_eventtypes():
                et_w = EventTypeWrapper()
                et_w.events = []
                et_w.eventtype = event_type
                for event in event_type.get_events().filter():
                    et_w.events.append(event)
                #raise AssertionError(et_w.events)
                org_w.eventtypes.append(et_w)
                del et_w

        elif type == 'event':
            type_display = _("Report grouped by Event")
        else:
            type_display = _("Report Types")
        
        # report code here
        context = {'current_org':current_org,'org_w':org_w,'type':type,'type_display':type_display,'form':form}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))



