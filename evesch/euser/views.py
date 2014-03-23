# Create your views here.
#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth import get_user_model
from evesch.euser.models import get_current_user
from evesch.euser.forms import UserForm
from evesch.event.models import EventType
from evesch.org.models import Organization
from evesch.event.forms import EventTypeForm
from evesch.euser.forms import UserForm
from evesch.core.lib import Message

@login_required
def user_view(request, username, template_name=None):
    current_user, message = get_current_user(username)
    if not message:
        if request.user.id == current_user.id:
            myprofile = True
        else:
            myprofile = False
        context = {'current_user':current_user,'myprofile':myprofile}
    else:
        template_name = "core/message.html"
        context = {'message':message,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))

@login_required
def user_settings(request, template_name=None):
    message = None
    quick_message = ""
    current_user = request.user
    show_dialog=False
    if request.method == 'POST':
        form = UserForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            message = Message(title=_("Settings Saved"), text=_("Settings Saved"))
            message.addlink(_("View"),reverse('euser_user_view',kwargs={'username':current_user.username,}))
            message.addlink(_("Edit"),reverse('euser_user_settings'))
            quick_message = _("Saved")
            if request.POST.get("dialog",'') == "False":
                template_name = "core/message.html"
                show_dialog=False
            else:
                show_dialog=True
    else:
            form = UserForm(instance=current_user)
    context = {'current_user':current_user,'form':form,'quick_message':quick_message,'message':message,'show_dialog':show_dialog,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))

@login_required
def lookup_users(request, org_short_name=None, template_name=None):
    users = []
    
    if org_short_name:
        current_user = request.user
        current_org, message = Organization.objects.get_current_org(org_short_name)
        if not message:
            operms = current_org.org_perms(current_user) 
            if not operms['is_memberof_org']:
                message = Message(title=_("Cannot View Group"), text=_("You are not a member of this org"))
        if not message:
            if request.GET.__contains__("q"): 
                try:
                    q  = request.GET['q']
                    users = (current_org.get_invited_users() | current_org.get_members()).filter(Q(username__icontains=q) | Q(last_name__icontains=q) | Q(first_name__icontains=q)).order_by('username')[:10]
                except ValueError:
                    pass              
    else:
        if request.GET.__contains__("q"): 
            try:
                q  = request.GET['q']
                users = get_user_model().objects.filter(Q(username__icontains=q) | Q(last_name__icontains=q) | Q(first_name__icontains=q)).order_by('username')[:10]
            except ValueError:
                pass
    
    context = {'users':users,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))
