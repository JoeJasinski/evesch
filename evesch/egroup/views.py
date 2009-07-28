# Create your views here.
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from euser.models import get_current_user
from egroup.models import UserGroup
from org.models import Organization
from egroup.forms import UserGroupEditForm, UserGroupForm
from core.lib import Message
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

@login_required
def group_add(request,org_short_name,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:    
        current_user, message = get_current_user(request.user)
    if not message:
        if not current_org.is_member(request.user):
            template_name = "core/message.html"
            message = Message(title=_("Cannot Add Group"), text=_("You cannot add a group in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_add_group']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Add Group"), text=_("You do not have permission to add a group in this organization."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            form = UserGroupForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.org_name = current_org
                new_form.group_removable=True
                new_form.save()
                
                template_name = "core/message.html"
                message = Message(title=_("Group Added"), text=_("You have added a group"))
                message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            #form = EventTypeForm(request.POST)
            #if form.is_valid():
                context = {'current_org':current_org,'message':message}
            else:
                context = {'current_org':current_org,'form':form,}
        else:
            form = UserGroupForm()
            #context = {'error':"User Add", 'form':form, }
            context = {'current_org':current_org, 'form':form,}
    else:
        template_name = "core/message.html"
        context = {'message':message,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))


@login_required
def group_edit(request, org_short_name, group_hash, template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_user, message = get_current_user(request.user)
    if not message: 
        current_usergroup, message = UserGroup.objects.get_current_usergroup(group_hash)
    if not message:
        if not current_org.is_member(request.user):
            template_name = "core/message.html"
            message = Message(title=_("Cannot Edit Group"), text=_("You cannot edit a group in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_edit_group']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Edit Group"), text=_("You do not have permission to edit a group in this organization."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            form = UserGroupEditForm(request.POST,instance=current_usergroup)
            #form.org_name = current_org
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
        else:
            form = UserGroupEditForm(instance=current_usergroup)
        context = {'current_org':current_org,'form':form}
    else:
        template_name = "core/message.html"
        context = {'message':message,'current_org':current_org,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))


@login_required
def group_remove(request, org_short_name, group_hash, template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_user, message = get_current_user(request.user)
    if not message: 
        current_usergroup, message = UserGroup.objects.get_current_usergroup(group_hash)
    if not message:   
        operms = current_org.org_perms(current_user) 
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Group"), text=_("You cannot remove a group in an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        if not operms['can_remove_group']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Event Type"), text=_("You do not have permission to remove a group in this organization."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            current_usergroup.delete()
            return HttpResponseRedirect(reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
        else:
            pass
        context = {'current_org':current_org,'current_usergroup':current_usergroup}
    else:
        template_name = "core/message.html"
        context = {'message':message,'current_org':current_org,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))

@login_required
def group_view(request, org_short_name, group_hash, template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_user, message = get_current_user(request.user)
    if not message: 
        current_usergroup, message = UserGroup.objects.get_current_usergroup(group_hash)
    if not message: 
        context = {'current_org':current_org,'current_usergroup':current_usergroup}
    else:
        template_name = "core/message.html"
        context = {'message':message,'current_org':current_org,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))