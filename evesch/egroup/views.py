# Create your views here.
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from euser.models import get_current_user
from egroup.models import UserGroup
from org.models import Organization
from euser.models import eUser
from egroup.forms import UserGroupEditForm, UserGroupForm, GroupAddMemberForm
from core.lib import Message, ePage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
import re

@login_required
def group_add(request,org_short_name,template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:    
        current_user, message = get_current_user(request.user)
    if not message:
        if not current_org.is_member(request.user):
            template_name = "core/message.html"
            message = Message(title=_("Cannot Add Group"), text=_("You cannot add a group in an organization that you do not belong to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_add_group']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Add Group"), text=_("You do not have permission to add a group in this organization."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        show_dialog=False
        if request.method == 'POST':
            form = UserGroupForm(request.POST)
            if form.is_valid():
                new_group= form.save(commit=False)
                new_group.org_name = current_org
                new_group.group_removable=True
                new_group.save()
                
                message = Message(title=_("Group Added"), text=_("You have added a group"))
                message.addlink(_("View"),current_org.get_absolute_url())
                message.addlink(_("Edit"),reverse('egroup_group_edit',kwargs={'org_short_name':current_org.org_short_name,'group_hash':new_group.group_hash}))
                if request.POST.get("dialog",'') == "False":
                    template_name = "core/message.html"
                    show_dialog=False
                else:
                    show_dialog=True
                context = {'current_org':current_org,'form':form,'message':message,'show_dialog':show_dialog,}
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
            message.addlink(_("Back"),current_org.get_absolute_url())
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['can_edit_group']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Edit Group"), text=_("You do not have permission to edit a group in this organization."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        groupuser_page = ePage(1)
        if request.GET.__contains__("groupuser_page"): 
            try:
                groupuser_page.curr  = int(request.GET['groupuser_page'])
            except:
                groupuser_page.curr = 1
        groupusers = current_usergroup.get_groupusers()
        groupuser_page.set_pages(Paginator(groupusers, 48))
        
        group_add_member_form = GroupAddMemberForm()
        edit_form = UserGroupEditForm(instance=current_usergroup)
        show_dialog=False
        if request.method == 'POST':
            
            #form.org_name = current_org
            action = request.POST.get('action','')
            p = re.compile('^[\w]{1,20}$')
            if not p.match(action):
                action = ""
            if action == 'group_edit':
                edit_form = UserGroupEditForm(request.POST,instance=current_usergroup)
                if edit_form.is_valid():
                    edit_form.save()
                    message = Message(title=_("Group Changes Saved"), text=_("Group Changes Saved"))
                    message.addlink(_("View"),reverse('egroup_group_view',kwargs={'org_short_name':current_org.org_short_name,'group_hash':current_usergroup.group_hash}))
                    message.addlink(_("Edit"),reverse('egroup_group_edit',kwargs={'org_short_name':current_org.org_short_name,'group_hash':current_usergroup.group_hash}))
                    #return HttpResponseRedirect(current_org.get_absolute_url())
                    if request.POST.get("dialog",'') == "False":
                        template_name = "core/message.html"
                        show_dialog=False
                    else:
                        show_dialog=True
            elif action == 'group_member_add':
                group_add_member_form = GroupAddMemberForm(request.POST)
                if group_add_member_form.is_valid():             
                    user_list = group_add_member_form.cleaned_data['user_list'].strip().strip(',').split(',')
                    new_user_list = []
                    for user in user_list:
                        new_user_list.append(user.strip().strip(','))
                    new_group_users = eUser.objects.filter(username__in=new_user_list)
                    for user in new_group_users:
                        user.user_groups.add(current_usergroup)
                    #raise AssertionError(new_group_users)
            else:
                pass
        else:
            pass
        context = {'current_org':current_org,'edit_form':edit_form, 'group_add_member_form':group_add_member_form, 'current_usergroup':current_usergroup, 'groupusers':groupuser_page,'message':message,'show_dialog':show_dialog, }
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
        if not current_usergroup.group_removable:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Default Group"), text=_("You cannot remove this group since it is a default group."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}            
    if not message:
        operms = current_org.org_perms(current_user) 
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Group"), text=_("You cannot remove a group in an organization that you do not belong to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if not operms['can_remove_group']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Event Type"), text=_("You do not have permission to remove a group in this organization."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if request.method == 'POST':
            current_usergroup.delete()
            return HttpResponseRedirect(current_org.get_absolute_url())
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
        groupuser_page = ePage(1)
        if request.GET.__contains__("groupuser_page"): 
            try:
                groupuser_page.curr  = int(request.GET['groupuser_page'])
            except:
                groupuser_page.curr = 1
        groupusers = current_usergroup.get_groupusers()
        groupuser_page.set_pages(Paginator(groupusers, 48))
        context = {'current_org':current_org,'current_usergroup':current_usergroup,'groupusers':groupuser_page}
    else:
        template_name = "core/message.html"
        context = {'message':message,'current_org':current_org,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))

 
@login_required
def groupuser_remove(request, org_short_name, group_hash, group_user, template_name=None):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        current_user, message = get_current_user(request.user)
    if not message: 
        current_usergroup, message = UserGroup.objects.get_current_usergroup(group_hash)
    if not message:
        group_user, message = get_current_user(group_user)
    if not message:
        operms = current_org.org_perms(current_user) 
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Group"), text=_("You cannot remove a group member in an organization that you do not belong to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if not operms['can_remove_groupmember']:
            template_name = "core/message.html"
            message = Message(title=_("Cannot Remove Event Type"), text=_("You do not have permission to remove a group member in this organization."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        #raise AssertionError(group_user)
        if group_user.get_user_groups().filter(id=current_usergroup.id):
            group_user.user_groups.remove(current_usergroup)
            return HttpResponseRedirect(reverse('egroup_group_edit',kwargs={'org_short_name':current_org.org_short_name,'group_hash':current_usergroup.group_hash,} ) )
        context  = {'current_org':current_org,'current_group':current_usergroup,}
    else:
        template_name = "core/message.html"
        context = {'message':message,'current_org':current_org,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))