# Create your views here.
from django.utils.translation import ugettext_lazy as _
from org.models import Organization
from org.forms import OrganizationForm, OrganizationFormEdit, OrganizationJoinForm, OrganizationInviteMember
from django.shortcuts import render_to_response
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from core.lib import Message, ePage
from egroup.models import UserGroup
from euser.models import User, get_current_user
from django.core.paginator import Paginator


@login_required
def orgs_list(request, template_name=None):       
    current_user, message = get_current_user(request.user)
    if not message:
        all_orgs_page = ePage(1)
        if request.GET.__contains__("all_orgs_page"): 
            try:
                all_orgs_page.curr  = int(request.GET['all_orgs_page'])
            except ValueError:
                all_orgs_page.curr = 1
        orgs = Organization.objects.filter(org_active=True).order_by('org_name')
        all_orgs_page.set_pages(Paginator(orgs, 3))

        my_orgs_page = ePage(1)
        if request.GET.__contains__("my_orgs_page"): 
            try:
                my_orgs_page.curr = int(request.GET['my_orgs_page'])
                #my_orgs_page.curr = int(request.GET.get('my_orgs_page',1))
            except ValueError:
                my_orgs_page.curr = 1 

        my_org_groups = UserGroup.objects.filter(pk__in=current_user.get_user_groups())
        my_groups = orgs.filter(group_set__in=my_org_groups)
        my_orgs = current_user.get_user_orgs().order_by('org_name')
        jaz_orgs = []
        for org in my_orgs:
            org.user_perms = org.org_perms(current_user)
            jaz_orgs.append(org)
        my_orgs_page.set_pages(Paginator(jaz_orgs, 3))

        #raise AssertionError(jaz_orgs[0].user_perms)
        context = {'message':_("Index"),
                   'all_orgs_page':all_orgs_page,
                   'my_groups':my_groups,
                   'my_orgs_page':my_orgs_page,
                   }
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context, context_instance=RequestContext(request))


@login_required
def orgs_list_all(request, template_name=None):       
    current_user, message = get_current_user(request.user)
    if not message:
        all_orgs_page = ePage(1)
        if request.GET.__contains__("all_orgs_page"): 
            try:
                all_orgs_page.curr  = int(request.GET['all_orgs_page'])
            except ValueError:
                all_orgs_page.curr = 1
        orgs = Organization.objects.filter(org_active=True).order_by('org_name')
        all_orgs_page.set_pages(Paginator(orgs, 3))
        context = {'all_orgs_page':all_orgs_page,}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context, context_instance=RequestContext(request))

@login_required
def orgs_list_my(request, template_name=None):       
    current_user, message = get_current_user(request.user)
    if not message:
        orgs = Organization.objects.filter(org_active=True).order_by('org_name')

        my_orgs_page = ePage(1)
        if request.GET.__contains__("my_orgs_page"): 
            try:
                my_orgs_page.curr = int(request.GET['my_orgs_page'])
            except ValueError:
                my_orgs_page.curr = 1 
        my_org_groups = UserGroup.objects.filter(pk__in=current_user.get_user_groups())
        my_groups = orgs.filter(group_set__in=my_org_groups)
        my_orgs = current_user.get_user_orgs().order_by('org_name')
        jaz_orgs = []
        for org in my_orgs:
            org.user_perms = org.org_perms(current_user)
            jaz_orgs.append(org)
        my_orgs_page.set_pages(Paginator(jaz_orgs, 3))

        #raise AssertionError(my_orgs_page.current_page().object_list)
        context = {'my_orgs_page':my_orgs_page,}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context, context_instance=RequestContext(request))



def org_join(request, org_short_name, template_name=None):
    current_user, message = get_current_user(request.user)
    if not message:
        current_org, message = Organization.objects.get_current_org(org_short_name, message)
    if not message:
        #if current_user.user_organizations.filter(org_short_name=org_short_name):
        if current_org.is_member(current_user):
            template_name = "core/message.html"
            message = Message(title=_("Already a Member"), text=_("You are already a member of this organization." ))          
            message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:  
        if request.method == 'POST':                    
            current_user.user_organizations.add(current_org)
            template_name = "core/message.html"
            #message = Message(title="You have Joined the organization", text="Org Join Successful: " + org_user_group.group_name )
            message = Message(title=_("You have Joined the organization"), text=_("Org Join Successful: %s" % (current_org.org_name,)) )            
            message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
        else:  
            form = OrganizationJoinForm()
            context = {'form':form,'current_org':current_org}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))

def org_leave(request, org_short_name, template_name=None):
    current_user, message = get_current_user(request.user)
    if not message:
        current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        #if current_user.user_organizations.filter(id=current_org.id):
        if current_org.is_member(current_user):
            if request.method == 'POST':
                current_user.user_organizations.remove(current_org)
                template_name = "core/message.html"
                message = Message(title=_("Left Organization"), text=_("You have left the Organization"))          
                message.addlink(_("Continue"),reverse('org_orgs_list',kwargs={}))
        else:
            template_name = "core/message.html"
            message = Message(title=_("Not a Member"), text=_("You cannot leave this organization because you are not a member of the organization."))      
            message.addlink(_("Back"),reverse('org_orgs_list',kwargs={}))               
        context = {'message':message, 'current_org':current_org, } 
    else:
        template_name = "core/message.html"
        context = {'message':message }      
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def org_view(request,org_short_name,template_name=None):
    """ Displays organization detail information """
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        org_eventtypes = current_org.eventtype_set.filter(type_active=True)
        context = {'message':_("Org View"),'current_org':current_org,'org_eventtypes':org_eventtypes}
    else:
        template_name = "core/message.html"
        context = {'message':message }    
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def org_edit(request,org_short_name=None,template_name=None):
    """ Edits and organization """
    
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:    
        current_user, message = get_current_user(request.user)
    if not message:
        if not current_org.is_member(current_user):
            template_name = "core/message.html"
            message = Message(title=_("Can Not Edit Org"), text=_("You cannot edit an organization that you do not belong to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_edit_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Edit Org"), text=_("You cannot edit this organization because you do not have permission to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            form = OrganizationFormEdit(request.POST, instance=current_org)
            if form.is_valid():
                form.save()
                template_name = "core/message.html"
                message = Message(title=_("Organization Changes Saved"), text=_("Organization Changes Saved"))
                message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
                context = {'message':message,}
            else:
                context = {'org_short_name':org_short_name,'form':form,'current_org':current_org}                
        else:
            form = OrganizationFormEdit(auto_id=False,instance=current_org)
            context = {'org_short_name':org_short_name,'form':form,'current_org':current_org}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name, context,context_instance=RequestContext(request))

@login_required
def org_remove(request,org_short_name=None,template_name=None):
    """ Removes an organization """
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:    
        current_user, message = get_current_user(request.user)
    if not message:
        if not current_org.is_member(current_user):
            template_name = "core/message.html"
            message = Message(title=_("Can Not Remove Org"), text=_("You cannot remove an organization that you do not belong to."))
            message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_remove_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Remove Org"), text=_("You cannot remove this organization because you do not have permission to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        context = {'current_org':current_org}
        if request.method == 'POST':
            current_org.org_active = False
            current_org.save()
            return HttpResponseRedirect(reverse('org_orgs_list',))
        else:
            pass
    else:
        template_name = "core/message.html"
        context = {'message':message }     
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def org_add(request,template_name=None):
    """ Adds an organization """
    
    current_user, message = get_current_user(request.user)
    if not message:  
        if request.method == 'POST':
            form = OrganizationForm(request.POST)
            if form.is_valid():
                current_org = form.save()
                current_org.save()
                groups = UserGroup.objects.init_org_groups(current_org, current_user)
    
                template_name = "core/message.html"
                message = Message(title=_("Organization Added"), text=_("Organization Added"))
                message.addlink(_("Continue"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
                context = {'message':message,}
            else:
                context = { 'form':form}
        else:
            form = OrganizationForm()
            context = { 'form':form } 
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))    

@login_required
def org_member_remove(request,org_short_name=None, username=None, template_name=None):
    current_user, message = get_current_user(request.user)
    if not message:
        current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_member, message = get_current_user(username)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_remove_users']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Remove Member"), text=_("You cannot remove this member because you do not have permission to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            current_member.user_organizations.remove(current_org)
            return HttpResponseRedirect(reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name}))
        else:
            pass
        context = {'current_org':current_org, 'current_member':current_member, }
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))    

@login_required
def org_member_invite(request,org_short_name=None, template_name=None):
    current_user, message = get_current_user(request.user)
    if not message:
        current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_invite_users']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Invite Member"), text=_("You cannot invite people to this organization because you do not have permission to."))
            message.addlink(_("Back"),reverse('org_org_view',kwargs={'org_short_name':current_org.org_short_name,}))
            context = {'message':message,}
    if not message:
        form = OrganizationInviteMember()
        context = {'current_org':current_org,'form':form,}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))    
