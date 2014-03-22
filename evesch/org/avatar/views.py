import os.path
from random import sample
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db.models import get_app
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib import messages
from evesch.core.lib import Message
from evesch.euser.models import get_current_user
from evesch.org.models import Organization
from evesch.org.avatar.models import Avatar, upload_file_path
from evesch.org.avatar.forms import PrimaryAvatarForm, DeleteAvatarForm, UploadAvatarForm

KEYS='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def _get_next(request):
    """
    The part that's the least straightforward about views in this module is how they 
    determine their redirects after they have finished computation.

    In short, they will try and determine the next place to go in the following order:

    1. If there is a variable named ``next`` in the *POST* parameters, the view will
    redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters, the view will
    redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers, the view will
    redirect to that previous page.
    """
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    if not next:
        next = request.path
    return next

def change(request, org_short_name, extra_context={}, next_override=None):
    message = None
    current_user = request.user
    current_org, message = Organization.objects.get_current_org(org_short_name, message)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Edit Org Photo"), text=_("You cannot edit an organization that you do not belong to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if not operms['can_edit_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Edit Org Photo"), text=_("You cannot edit this organization because you do not have permission to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        avatars = Avatar.objects.filter(org=current_org).order_by('-primary')
        if avatars.count() > 0:
            avatar = avatars[0]
            kwargs = {'initial': {'choice': avatar.id}}
        else:
            avatar = None
            kwargs = {}
        primary_avatar_form = PrimaryAvatarForm( None, org=current_org, **kwargs)
        upload_avatar_form = UploadAvatarForm()
        if request.method == "POST":
            updated = False
            if 'avatar' in request.FILES:
                if avatars.count() >= 4:
                    template_name = "core/message.html"
                    message = Message(title=_("Max uploads reached"), text=_("You cannot upload more than 4 photos."))
                    message.addlink(_("Back"),reverse('org_org_edit_photo',kwargs={'org_short_name':current_org.org_short_name}))
                    message.addlink(_("Delete Photos"),reverse('org_org_delete_photo',kwargs={'org_short_name':current_org.org_short_name}))
                if not message:
                    upload_avatar_form = UploadAvatarForm(request.POST, request.FILES)
                    if upload_avatar_form.is_valid():
                        photo = Avatar(org=current_org, primary=True, avatar=upload_avatar_form.cleaned_data['avatar'],)
                        photo.save()
                        updated = True
                        messages.add_message(request, messages.INFO, _("Successfully uploaded a new organization photo."))
                        return HttpResponseRedirect(next_override or _get_next(request))
                else:
                    template_name = "core/message.html"
                    context = {'message':message }
                    return render_to_response(template_name,context,context_instance=RequestContext(request))                     
            if 'choice' in request.POST:
                primary_avatar_form = PrimaryAvatarForm(request.POST or None, org=current_org, **kwargs)
                if primary_avatar_form.is_valid():
                    avatar = Avatar.objects.get(id=primary_avatar_form.cleaned_data['choice'])
                    avatar.primary = True
                    avatar.save()
                    updated = True
                    messages.add_message(request, messages.INFO, _("Successfully updated the organization photo."))
                    return HttpResponseRedirect(next_override or _get_next(request))
        
        template_name='avatar/change.html'
        context = { 'current_org':current_org, 'avatar': avatar, 'avatars': avatars,'primary_avatar_form': primary_avatar_form,
                  'upload_avatar_form':upload_avatar_form,'next': next_override or _get_next(request), }
    else:
        template_name = "core/message.html"
        context = {'message':message } 
    return render_to_response(template_name,context,context_instance=RequestContext(request))

change = login_required(change)

def delete(request, org_short_name, extra_context={}, next_override=None):
    current_user = request.user
    message = None
    current_org, message = Organization.objects.get_current_org(org_short_name, message)
    if not message:
        operms = current_org.org_perms(current_user)
        if not operms['is_memberof_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Edit Org Photo"), text=_("You cannot edit an organization that you do not belong to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:
        if not operms['can_edit_org']:
            template_name = "core/message.html"
            message = Message(title=_("Can Not Edit Org Photo"), text=_("You cannot edit this organization because you do not have permission to."))
            message.addlink(_("Back"),current_org.get_absolute_url())
            context = {'message':message,}
    if not message:        
        avatars = Avatar.objects.filter(org=current_org).order_by('-primary')
        if avatars.count() > 0:
            avatar = avatars[0]
        else:
            avatar = None
        delete_avatar_form = DeleteAvatarForm(request.POST or None, org=current_org)
        if request.method == 'POST':
            if delete_avatar_form.is_valid():
                ids = delete_avatar_form.cleaned_data['choices']
                if unicode(avatar.id) in ids and avatars.count() > len(ids):
                    for a in avatars:
                        if unicode(a.id) not in ids:
                            a.primary = True
                            a.save()
                            break
                Avatar.objects.filter(id__in=ids).delete()
                messages.add_message(request, messages.INFO, _("Successfully deleted the requested avatars."))
                return HttpResponseRedirect(next_override or _get_next(request))
        return render_to_response('avatar/confirm_delete.html',extra_context,
            context_instance = RequestContext(request,
                { 'avatar': avatar, 'avatars': avatars,'current_org':current_org,
                  'delete_avatar_form': delete_avatar_form,'next': next_override or _get_next(request), }
            )
        )
    else:
        template_name = "core/message.html"
        context = {'message':message } 
    return render_to_response('avatar/confirm_delete.html',context,context_instance=RequestContext(request))
delete = login_required(delete)
