# Create your views here.
from django.utils.translation import ugettext_lazy as _
from org.models import Organization
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from event.models import Attendee, Event
from euser.models import User 
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from core.forms import EveschLoginForm, SignupForm, PasswordResetForm
from core.lib import Message, ePage
from django.core.paginator import Paginator

def index(request,template_name=None):
    #raise AssertionError(request.user)
    if request.user.is_authenticated():

        try:
            current_user = User.objects.get(username=request.user)
            attending = current_user.get_attending_events()
            user_events = Event.objects.filter(attendee__in=attending)
            #user_signups = current_user.get_attending_events() #Attendee.objects.filter(att_name=current_user)
            #user_events = Event.objects.filter(attendee__att_name__in=user_signups).filter(event_date__gte=datetime.now()).order_by('event_date')    
            #user_events = []
            #user_events = []
            #for att in user_signups:
            #    user_events.append(att.att_event)
            #    user_events = (user_events | att.att_event) #.filter(event_date__gte=datetime.now()).order_by('event_date')
                
            user_orgs = current_user.get_user_orgs().order_by('org_name')
    
            my_orgs_page = ePage(1)
            if request.GET.__contains__("my_orgs_page"): 
                try:
                    my_orgs_page.curr = int(request.GET['my_orgs_page'])
                except:
                    my_orgs_page.curr = 1 
    
            my_orgs_page.set_pages(Paginator(user_orgs, 3))
    
            context = {'user_events':user_events,'my_orgs_page':my_orgs_page,'ajax_page_my':reverse('org_orgs_list_my_ajax',kwargs={}),}
        except ObjectDoesNotExist:
            template_name = "error.html"
            context = {'error':_("User does not exist ") } 
            return HttpResponseRedirect(reverse('account_auth_login'))
    else:
        template_name="index_anonymous.html"
        context={}
    
    return render_to_response(template_name,context,context_instance=RequestContext(request))


def evesch_login(request, template_name=None):
    if request.POST:
        form = EveschLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                    # Redirect to a success page.
                else:
                    template_name = "core/message.html"
                    message = Message(title=_("Disabled Account"), text=_("Disabled Account"))
                    message.addlink(_("Back"),reverse('home'))
                    context = {'message':message,}
            else:
                template_name = "core/message.html"
                message = Message(title=_("Invalid Login"), text=_("Invalid Login"))
                message.addlink(_("Back"),reverse('home'))
                context = {'message':message,}
        else:
            form = EveschLoginForm()
            context = {'form':form,}
    else:
        form = EveschLoginForm()
        context = {'form':form}
    return render_to_response(template_name,context,context_instance=RequestContext(request))
        # Return an 'invalid login' error message.

def evesch_logout(request, template_name=None):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def evesch_signup(request, template_name=None):
    if request.user.is_authenticated():
        template_name = "core/message.html"
        message = Message(title=_("Cannot Signup"), text=_("You cannot signup for a new user account while logged in."))
        message.addlink(_("Back"),reverse('home'))
        context = {'message':message,}
    else:
        if request.POST:
            form = SignupForm(request.POST)
        else: 
            form = SignupForm()
        context = {'form':form,}
    return render_to_response(template_name,context,context_instance=RequestContext(request)) 

def evesch_password_reset(request, template_name=None):
    if request.POST:
        form = PasswordResetForm(request.POST)
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        return HttpResponseRedirect(reverse('home'))
    else: 
        form = PasswordResetForm()
    context = {'form':form,}
    return render_to_response(template_name,context,context_instance=RequestContext(request)) 
 

def error(request,template_name):
    return render_to_response("error.html",{'error':_("Error")})

def page_not_found(request,template_name):
    return render_to_response(template_name,{'message':_("Page Not Found")},context_instance=RequestContext(request))
