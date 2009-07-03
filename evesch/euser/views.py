# Create your views here.
#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from euser.models import User, get_current_user
from event.models import EventType
from event.forms import EventTypeForm
from euser.forms import UserForm
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q


def get_or_create_profile(self,user):
    try:
        profile = user.get_profile()
    except ObjectDoesNotExist:
        profile = User(username=user,phone='')
        profile.save()
    return profile

def users_list(request, template_name=None):
    context = {'error':_("User List")}
    return render_to_response(template_name,context, context_instance=RequestContext(request))

@login_required
def user_add(request,template_name=None):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            return render_to_response("error.html",{'error':_("Add not implemented")})
    else:
        form = UserForm()
        context = {'error':"User Add", 'form':form, }
        return render_to_response(template_name,context, context_instance=RequestContext(request))

@login_required
def user_view(request,username, template_name=None):
    current_user, message = get_current_user(username)
    if request.user.id == current_user.id:
        myprofile = True
    else:
        myprofile = False
        
        
    context = {'current_user':current_user,'myprofile':myprofile}
    return render_to_response(template_name,context, context_instance=RequestContext(request))

@login_required
def lookup_users(request, template_name=None):
    users = []
    
    if request.GET.__contains__("q"): 
        try:
            q  = request.GET['q']
            users = User.objects.filter(Q(username__contains=q) | Q(last_name__contains=q) | Q(first_name__contains=q)).order_by('username')[:10]
        except ValueError:
            pass
    
    context = {'users':users,}
    return render_to_response(template_name,context, context_instance=RequestContext(request))
