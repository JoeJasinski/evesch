# Create your views here.
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from core.lib import Message
from core.exceptions import EventTypeExistsException
from core.forms import MessageForm
from event.models import Event,EventType,Attendee
from event.forms import EventForm, EventEditForm, EventTypeForm, AttendeeForm
from euser.models import User, get_current_user
from org.models import Organization


@login_required
def events_list(request,org_short_name,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    current_event_type_flag = False
    filteron_past_events = False
    if not message:
        if request.GET.__contains__("event_type"): 
            try:
                filteron_type = request.GET['event_type']
                #current_event_type = EventType.objects.get(org_name=current_org,type_name=filteron_type)
                current_event_type = current_org.get_eventtypes().get(type_name=filteron_type)
                current_event_type_flag = True
            except:
                pass
            
        if request.GET.__contains__("past_events"):
            try:
                filteron_past_events = request.GET['past_events']
            except:
                pass
   
        if current_event_type_flag:
            events = current_org.get_events().order_by('event_date').filter(event_type = current_event_type)
            heading =  "%s Events List" % (current_event_type.type_name,)
        else:
            events = current_org.get_events() 
            heading = "Events List" 
            
        if filteron_past_events:
            events = events.filter(event_date__lt=datetime.now()).order_by('-event_date')            
        else:
            events = events.filter(event_date__gte=datetime.now()).order_by('event_date')  
            
        context = { 'events':events, 'current_org':current_org, 'heading':heading, }
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name, context,context_instance=RequestContext(request))         

@login_required
def event_add(request,org_short_name,template_name=None):
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
        if not operms['can_add_event']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Add Event"), text=_("You do not have permission to add an event in this organization."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        current_user, message = get_current_user(request.user, message)
    if not message:
        if request.method == 'POST':
            form = EventForm(current_org,request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.event_creator_name = current_user
                new_form.event_org = current_org
                new_form.save()

                template_name = "core/message.html"
                message = Message(title=_("Event Add Successful"), text=_("Event Add Successful"))            
                message.addlink(_("Continue"),reverse('event_events_list',kwargs={'org_short_name':current_org.org_short_name,}))
                context = {'message':message,}               
            else:
                context = {'form':form,'current_org':current_org,'org_short_name':org_short_name,'error':"update"}
        else:
            form = EventForm(current_org)
            context = {'form':form,'current_org':current_org,'org_short_name':org_short_name}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name, context, context_instance=RequestContext(request))

@login_required
def event_edit(request,org_short_name,event_hash,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_event, message = current_org.get_current_event(event_hash, message) 
    if not message:    
        current_user, message = get_current_user(request.user)
    if not message:
        eperms = current_event.event_perms(current_user)
        if not eperms['can_edit_event']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Edit Event"), text=_("You do not have permission to edit this event"))        
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Edit Event"), text=_("You cannot edit an event in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            form = EventEditForm(current_org, request.POST, instance=current_event)
            if form.is_valid():
                form.save()
                template_name = "core/message.html"
                message = Message(title=_("Event Saved"), text=_("Event Saved"))
                message.addlink(_("Continue"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
                message.addlink(_("Edit"),reverse('event_event_edit',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
                context = {'message':message,}
            if not message:
                message = None
            context = {'form':form,'current_org':current_org,'event':current_event,'message':message,}
        else:
            form = EventEditForm(current_org,auto_id=False,instance=current_event)
            context = {'form':form,'current_org':current_org,'event':current_event,}
    else:
        template_name = "core/message.html"
        context =  {'message':message }
    return render_to_response(template_name, context, context_instance=RequestContext(request))  

@login_required
def event_remove(request,org_short_name,event_hash,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_event, message = current_org.get_current_event(event_hash, message) 
    if not message:    
        current_user, message = get_current_user(request.user)
    if not message:
        eperms = current_event.event_perms(current_user)
        if not eperms['can_remove_event']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Delete Event"), text=_("You do not have permission to delete this event"))        
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}
    if not message:    
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Event"), text=_("You cannot remove an event in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,'current_event':current_event}
    if not message:
        if request.method == 'POST':
            current_event.event_active = False
            current_event.save()
            return HttpResponseRedirect(reverse('event_events_list',kwargs={'org_short_name':current_org.org_short_name,}))
        else:
            context = {'current_org':current_org,'current_event':current_event }
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def event_attendee_add(request,org_short_name,event_hash,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_event, message = current_org.get_current_event(event_hash, message)
    if not message:
        current_user, message = get_current_user(request.user, message)
    if not message:    
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Attend Event"), text=_("You cannot register for an event in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}
    if not message:
        if not current_event.event_open:
            template_name = "core/message.html"
            text = _("This event is closed.  Contact the event coordinator with comments or concerns.")
            message = Message(title=_("Event Closed", text=text))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,} 
    if not message:
        if not current_event.is_within_signup_deadline():
            template_name = "core/message.html"
            text = _("You may not register for this event after " + current_event.event_signup_deadline.strftime("%A %m/%d/%Y"))
            message = Message(title=_("Attendee Add Error", text=text))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}
    if not message:
        if Attendee.objects.filter(att_name=current_user,att_event=current_event):
            template_name = "core/message.html"
            message = Message(title=_("Already Registered"), text=_("Attendee is already registered"))           
            message.addlink(_("Continue"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}  
    if not message:
        if request.method == 'POST':
            form = AttendeeForm(current_event,request.POST)

            #raise AssertionError(form.data)
            if form.is_valid(): 
                attendee = form.save(commit=False)
                attendee.att_name = current_user
                attendee.att_event = current_event
                attendee.att_ip = request.META['REMOTE_ADDR'] 
                attendee.att_added_date = datetime.now()
                if current_event.event_track_hours:
                    attendee.att_hours = form.cleaned_data["att_hours"]
                if current_event.att_header_col1:
                    attendee.att_col1 = form.cleaned_data["att_col1"]
                if current_event.att_header_col2:
                    attendee.att_col2 = form.cleaned_data["att_col2"]
                if current_event.att_header_col3:
                    attendee.att_col3 = form.cleaned_data["att_col3"]
                if current_event.att_header_col4:
                    attendee.att_col4 = form.cleaned_data["att_col4"]
                if current_event.att_header_col5:
                    attendee.att_col5 = form.cleaned_data["att_col5"]
                if current_event.att_header_col6:
                    attendee.att_col6 = form.cleaned_data["att_col6"]                
                attendee.save()
                #context = {'current_org':current_org,'current_event':current_event,'current_user':current_user,'form':form }
                template_name = "core/message.html"
                message = Message(title=_("Registration Complete"), text=_("You have Registered for this event"))           
                message.addlink(_("Continue"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
                context = {'message':message,}
            else:                                    
                context = {'current_org':current_org,'current_event':current_event,'current_user':current_user,'form':form }
        else:
            form = AttendeeForm(current_event)
            context = {'current_org':current_org,'current_event':current_event,'current_user':current_user,'form':form }
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def event_attendees_message(request,org_short_name,event_hash,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_event, message = current_org.get_current_event(event_hash, message)
    if not message:
        current_user, message = get_current_user(request.user, message)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Message Users"), text=_("You cannot message users in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}
    if not message:
        eperms = current_event.event_perms(current_user)
        if not eperms['can_message_event']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Message Users"), text=_("You cannot message users unless you are attending the event."))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}
    if not message:
        attendees = current_event.get_attendees()  #attendee_set.all()
        if not attendees:
            message = Message(title=_("No attendees"), text=_("No attendees are signed up for this event."))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':event_hash}))
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                body = form.cleaned_data['body']
                template_name = "core/message.html"
                message = Message(title=_("Message Sent"), text=_("Message Sent"))          
                message.addlink("Continue",reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':event_hash}))
                context = {'message':message,}
            else:
                context = {'attendees':attendees,'form':form, 'current_event':current_event }
        else:
            form = MessageForm()
            context = {'attendees':attendees,'form':form, 'current_event':current_event }
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def event_attendee_remove(request,org_short_name,event_hash,att_name,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_event, message = current_org.get_current_event(event_hash, message)
    if not message:
        current_user, message = get_current_user(request.user, message)
    if not message:    
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove User from Event"), text=_("You cannot remove a user from  an event in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}
    if not message:
        try:
            current_attendee = current_event.attendee_set.get(att_name=User.objects.get(username=att_name))
        except ObjectDoesNotExist:
            message = Message(title=_("Cannot Remove User from Event"), text=_("This user is not attending this event."))
            context = {'error':_("Attendee does not exist"),'org_short_name':org_short_name}
            return render_to_response("error.html",context,context_instance=RequestContext(request))
    if not message:
        aperms = current_attendee.att_perms(current_user)
        if not aperms['can_remove_attendee']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove User from Event"), text=_("You do not have permission to remove this attendee."))
            message.addlink(_("Back"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}
        if request.method == 'POST':
            current_attendee.delete()
            template_name = "core/message.html"
            message = Message(title=_("Attendee Removed"), text=_("Attendee Removed"))          
            message.addlink(_("Continue"),reverse('event_event_view',kwargs={'org_short_name':current_org.org_short_name,'event_hash':current_event.event_hash}))
            context = {'message':message,}  
        else:
            #raise AssertionError('GOT HERE ' + str(aperms))
            template_name="event/event_attendee_remove.html"
            context = {'current_org':current_org,'event':current_event,'current_attendee':current_attendee}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def eventtype_add(request,org_short_name,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:    
        if not current_org.is_member(request.user):
            template_name = "core/message.html"
            message = Message(title=_("Cannot Add Event Type"), text=_("You cannot add an event type in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        current_user, message = get_current_user(request.user, message)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_add_type']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Add Event Type"), text=_("You do not have permission to add an event type in this organization."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            form = EventTypeForm(request.POST)
            if form.is_valid():
                type_name = form.cleaned_data['type_name']
                type_desc = form.cleaned_data['type_desc']
                type_color = form.cleaned_data['type_color']
                try:
                    et1 = EventType.objects.create_eventtype(type_name=type_name, org_name=current_org, type_desc=type_desc,type_color=type_color)
                    template_name = "core/message.html"
                    message = Message(title=_("Add Event Type Successful"), text=_("Add Event Type Successful"))          
                    message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
                    context = {'message':message,}  
                except ObjectDoesNotExist:
                    template_name = "core/message.html"
                    message = Message(title=_("Add Event Type Not Successful"), text=_("Add Event Type Not Successful"))           
                    message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
                    context = {'message':message,}                     
                except EventTypeExistsException:
                    template_name = "core/message.html"
                    message = Message(title=_("Event Type already exists"), text=_("Event Type already exists"))
                    message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
                    context = {'message':message,}                                         
                except: 
                    template_name = "core/message.html"
                    message = Message(title=_("Unknown Error"), text=_("Unknown Error"))
                    message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
                    context = {'message':message,}                           
            else:
                context = {'form':form, 'current_org':current_org}
        else:    
            form = EventTypeForm()
            context = {'form':form, 'org_short_name':org_short_name,'current_org':current_org}
                #raise AssertionError        
    else:
        context = {'message':message,} 
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def eventtype_edit(request, org_short_name,eventtype_hash,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_user, message = get_current_user(request.user, message)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_edit_type']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Edit Event Type"), text=_("You do not have permission to edit an event type in this organization."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:    
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Edit Event Type"), text=_("You cannot edit a event type in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        try:
            event_type = current_org.eventtype_set.get(type_hash=eventtype_hash, type_active=True)
            if request.method == 'POST':
                form = EventTypeForm(request.POST)
                if form.is_valid():
                    event_type.type_name = form.cleaned_data['type_name']
                    event_type.type_desc = form.cleaned_data['type_desc']
                    event_type.type_color = form.cleaned_data['type_color']
                    #event_type.type_active = form.cleaned_data['type_active']
                    event_type.save()
                    template_name = "core/message.html"
                    message = Message(title=_("Event Type Edit Successful"), text=_("Event Type Edit Successful"))
                    message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
                    message.addlink(_("Edit"),reverse('event_eventtype_edit',kwargs={'org_short_name':current_org.org_short_name,'eventtype_hash':event_type.type_hash}))
                    context = {'message':message,}  
                else:
                    context = {'current_org':current_org,'event_type':event_type,'form':form}
            else:
                form = EventTypeForm(auto_id=False,instance=event_type)
                context = {'current_org':current_org,'event_type':event_type,'form':form}
        except ObjectDoesNotExist:
            template_name = "error.html"
            context = {'error':_("Event Type does not exist") }
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name, context,context_instance=RequestContext(request))

@login_required
def eventtype_remove(request, org_short_name,eventtype_hash,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_user, message = get_current_user(request.user, message)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_remove_type']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Event Type"), text=_("You do not have permission to remove an event type in this organization."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:    
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Event Type"), text=_("You cannot remove an event type in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        try:
            event_type = current_org.eventtype_set.get(type_hash=eventtype_hash)
            if request.method == 'POST':
                event_type.type_active = False
                event_type.save()
                return HttpResponseRedirect(reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            else:
                context = {'current_org':current_org,'event_type':event_type }
        except ObjectDoesNotExist:
            template_name = "error.html"
            context = {'error':_("Event Type does not exist ")} 
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))
        
@login_required
def event_view(request,org_short_name,event_hash,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_event, message = current_org.get_current_event(event_hash, message)
    if not message:
        attendees = current_event.get_attendees()
        context = {'current_org':current_org,'current_event':current_event,'attendees':attendees,}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))
