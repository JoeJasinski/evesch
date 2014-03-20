# Create your views here.
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from evesch.core.lib import Message, ePage
from evesch.egroup.models import UserGroup
from evesch.euser.models import eUser, get_current_user
from evesch.org.models import Organization, OrgInvite
from evesch.event.models import EventType
from evesch.org.forms import OrganizationForm, OrganizationFormEdit, OrganizationJoinForm, OrganizationInviteMember


def org_browse(request, filter_abc=None, template_name=None):
    public_orgs = Organization.objects.get_browsable_orgs()
    if filter_abc:
        raise AssertionError(filter_abc)
        public_orgs = public_orgs.filter(org_name__istartswith=filter_abc)
    context = {'orgs':public_orgs,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))


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
            except:
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
                   'ajax_page_my':reverse('org_orgs_list_my_ajax',kwargs={}),
                   'ajax_page_all':reverse('org_orgs_list_all_ajax',kwargs={}),
                   }
    else:
        template_name = "core/message.html"
        context = {'message':message }
        
    return render_to_response(template_name,context, context_instance=RequestContext(request))


@login_required
def orgs_list_all(request, template_name=None):    
    message = None
    if not request.is_ajax():
        template_name = "core/message.html"
        message = Message(title=_("Cannot Be Viewed"), text=_("Cannot view this page" ))          
        context = {'message':message,}
    if not message:   
        current_user, message = get_current_user(request.user)
    if not message:
        all_orgs_page = ePage(1)
        if request.GET.__contains__("all_orgs_page"): 
            try:
                all_orgs_page.curr  = int(request.GET['all_orgs_page'])
            except:
                all_orgs_page.curr = 1
        orgs = Organization.objects.filter(org_active=True).order_by('org_name')
        all_orgs_page.set_pages(Paginator(orgs, 3))
        context = {'all_orgs_page':all_orgs_page, 'ajax_page_all':reverse('org_orgs_list_all_ajax',kwargs={}),}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context, context_instance=RequestContext(request))

@login_required
def orgs_list_my(request, template_name=None):
    message = None
    if not request.is_ajax():
        template_name = "core/message.html"
        message = Message(title=_("Cannot Be Viewed"), text=_("Cannot view this page" ))          
        context = {'message':message,}
    if not message:
        current_user, message = get_current_user(request.user)
    if not message:
        orgs = Organization.objects.filter(org_active=True).order_by('org_name')

        my_orgs_page = ePage(1)
        if request.GET.__contains__("my_orgs_page"): 
            try:
                my_orgs_page.curr = int(request.GET['my_orgs_page'])
            except:
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
        context = {'my_orgs_page':my_orgs_page,'ajax_page_my':reverse('org_orgs_list_my_ajax',kwargs={}),}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context, context_instance=RequestContext(request))

@login_required
def org_join(request, org_short_name, template_name=None):
    current_user, message = get_current_user(request.user)
    if not message:
        current_org, message = Organization.objects.get_current_org(org_short_name, message)
    if not message:
        operms = current_org.org_perms(current_user)
        if operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Already a Member"), text=_("You are already a member of this organization." ))          
            message.addlink(_("Continue"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if not operms['can_join_org']:
            template_name = "core/message.html"
            message = Message(title=_("Approval Needed"), text=_("In order to join this organization, you need approval from the organization admin."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:  
        if request.method == 'POST':                    
            current_user.user_organizations.add(current_org)
            current_user.user_invites_set.filter(org=current_org).delete()

            template_name = "core/message.html"
            #message = Message(title="You have Joined the organization", text="Org Join Successful: " + org_user_group.group_name )
            message = Message(title=_("You have Joined the organization"), text=_("Org Join Successful: %s" % (current_org.org_name,)) )            
            message.addlink(_("Continue"),current_org.get_absolute_url())
            context = {'message':message,}
        else:  
            form = OrganizationJoinForm()
            context = {'form':form,'current_org':current_org}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def org_leave(request, org_short_name, template_name=None):
    current_user, message = get_current_user(request.user)
    if not message:
        current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        operms = current_org.org_perms(current_user)
        if operms['is_memberof_org']:
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
        members_page = ePage(1)
        if request.GET.__contains__("members_page"): 
            try:
                members_page.curr  = int(request.GET['members_page'])
            except:
                members_page.curr = 1
        members = current_org.get_members()
        members_page.set_pages(Paginator(members, 48))
        #raise AssertionError(members_page.prev)
        
        org_eventtypes = current_org.get_eventtypes()
        context = {'message':_("Org View"),'current_org':current_org,'org_eventtypes':org_eventtypes, 'members':members_page, 'ajax_page_members': reverse('org_org_user_list_ajax', kwargs={'org_short_name':current_org.org_short_name,})}
    else:
        template_name = "core/message.html"
        context = {'message':message }    
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def org_members(request,org_short_name,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:    
        current_user, message = get_current_user(request.user)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Edit Org"), text=_("You cannot view members of an organization that you do not belong to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        members_page = ePage(1)
        if request.GET.__contains__("members_page"): 
            try:
                members_page.curr  = int(request.GET['members_page'])
            except:
                members_page.curr = 1
        members = current_org.get_members()
        members_page.set_pages(Paginator(members, 48))
        context = {'current_org':current_org,'members':members_page,'ajax_page_members': reverse('org_org_user_list_ajax', kwargs={'org_short_name':current_org.org_short_name,})}
    else:
        template_name = "core/message.html"
        context = {'message':message }  
    return render_to_response(template_name,context,context_instance=RequestContext(request))


@login_required
def org_edit(request,org_short_name=None,template_name=None):
    """ Edits an organization """
    
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:    
        current_user, message = get_current_user(request.user)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Edit Org"), text=_("You cannot edit an organization that you do not belong to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if not operms['can_edit_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Edit Org"), text=_("You cannot edit this organization because you do not have permission to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        show_dialog=False
        if request.method == 'POST':
            form = OrganizationFormEdit(request.POST, instance=current_org)
            if form.is_valid():
                form.save()
                message = Message(title=_("Organization Changes Saved"), text=_("Organization Changes Saved"))
                message.addlink(_("View"),current_org.get_absolute_url())
                message.addlink(_("Edit"),reverse('org_org_edit',kwargs={'org_short_name':current_org.org_short_name,}))
                if request.POST.get("dialog",'') == "False":
                    template_name = "core/message.html"
                    show_dialog=False
                else:
                    show_dialog=True
            context = {'org_short_name':org_short_name,'form':form,'current_org':current_org,'message':message,'show_dialog':show_dialog,}                
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
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Remove Org"), text=_("You cannot remove an organization that you do not belong to."))
            message.addlink(_("Continue"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if not operms['can_remove_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Remove Org"), text=_("You cannot remove this organization because you do not have permission to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
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
        show_dialog=False        
        if request.method == 'POST':
            form = OrganizationForm(request.POST)
            if form.is_valid():
                current_org = form.save()
                current_org.save()
                groups = UserGroup.objects.init_org_groups(current_org, current_user)
                eventtypes = EventType.objects.init_event_types(current_org)
    
                message = Message(title=_("Organization Added"), text=_("Organization Added"))
                message.addlink(_("View"),current_org.get_absolute_url())
                message.addlink(_("Edit"),reverse('org_org_edit',kwargs={'org_short_name':current_org.org_short_name,}))
                if request.POST.get("dialog",'') == "False":
                    template_name = "core/message.html"
                    show_dialog=False
                else:
                    show_dialog=True
                context = {'message':message,'current_org':current_org,'form':form,'show_dialog':show_dialog,}                    
            else:
                context = { 'form':form,'show_dialog':show_dialog,}
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
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Remove User"), text=_("You cannot remove a user in an organization that you do not belong to."))
            message.addlink(_("Continue"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if not operms['can_remove_users']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Remove Member"), text=_("You cannot remove this member because you do not have permission to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            current_member.user_organizations.remove(current_org)
            return HttpResponseRedirect(current_org.get_absolute_url())
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
    invited_users = eUser.objects.none()
    if not message:
        current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Invite User"), text=_("You cannot invite a user to an organization that you do not belong to."))
            message.addlink(_("Continue"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if not operms['can_invite_users']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Invite Member"), text=_("You cannot invite people to this organization because you do not have permission to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        invited_users_page = ePage(1)
        org_invites = current_org.invite_set.all()
        invited_users = eUser.objects.filter(user_invites_set__in=org_invites)       
        if request.method == 'POST':
            form = OrganizationInviteMember(request.POST)
            if form.is_valid():
                user_list = form.cleaned_data['invite_list'].strip().strip(',').split(',')
                new_user_list = []
                for user in user_list:
                    new_user_list.append(user.strip().strip(','))
                new_invited_users = eUser.objects.filter(username__in=new_user_list).exclude(user_invites_set__in=org_invites)
                for user in new_invited_users:
                    i = OrgInvite()
                    i.user = user
                    i.org = current_org
                    i.direction = True
                    i.save()
                invited_users = invited_users | new_invited_users  
        else:
            form = OrganizationInviteMember()

            if request.GET.__contains__("members_page"): 
                try:
                    members_page.curr = int(request.GET['members_page'])
                except:
                    members_page.curr = 1 
                
        invited_users_page.set_pages(Paginator(invited_users, 5))

        context = {'current_org':current_org,'form':form,'invited_users':invited_users_page,'ajax_page_members':reverse('org_org_invites_list_ajax', kwargs={'org_short_name':current_org.org_short_name,})}
    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))   

def org_list_invites(request,org_short_name,template_name=None):
    invited_users_page = ePage(1)
    message = None
    if not True: # request.is_ajax():
        template_name = "core/message.html"
        message = Message(title=_("Cannot Be Viewed"), text=_("Cannot view this page" ))          
        context = {'message':message,}
    if not message:
        current_user, message = get_current_user(request.user)
    if not message:
        current_org, message = Organization.objects.get_current_org(org_short_name)      
    if not message:
        if request.GET.__contains__("invited_users_page"): 
            try:
                invited_users_page.curr = int(request.GET['invited_users_page'])
            except:
                invited_users_page.curr = 1 

        org_invites = current_org.invite_set.all()
        invited_users = eUser.objects.filter(user_invites_set__in=org_invites)   
        invited_users_page.set_pages(Paginator(invited_users, 5))
        context = {'current_org':current_org,'invited_users':invited_users_page,'ajax_page_members':reverse('org_org_invites_list_ajax', kwargs={'org_short_name':current_org.org_short_name,})}

    else:
        template_name = "core/message.html"
        context = {'message':message }
    return render_to_response(template_name,context,context_instance=RequestContext(request))

   
