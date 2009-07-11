# Create your views here.
from django.utils.translation import ugettext_lazy as _
from org.models import Organization
from django.shortcuts import render_to_response 
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from event.models import Attendee, Event
from euser.models import User, UserEmail
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from core.forms import EveschLoginForm, SignupForm, PasswordResetForm, SignupConfirmForm
from core.lib import Message, ePage
from django.core.paginator import Paginator
import settings 
import random
import threading
from django.core.mail import send_mail


KEYS='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def index(request,template_name=None):
    #raise AssertionError(request.user)
    if request.user.is_authenticated():

        try:
            current_user = User.objects.get(username=request.user)
            attending = current_user.get_attending_events()
            user_events = Event.objects.filter(attendee__in=attending)
   
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
            session_captcha = request.session.get('signup_captcha', '-1')
            #raise AssertionError(session_captcha)
            form = SignupForm(session_captcha, request.POST)
            if form.is_valid():
                post_email = form.cleaned_data['email']
                post_username = form.cleaned_data['username']
                post_password = form.cleaned_data['password']
                user_email = UserEmail(email_label = 'primary', email_address=post_email,email_isDefault=True)
                user_email.save()
                user = User(username=post_username,email_addresses=user_email)
                user.first_name = post_username
                user.last_name = ''
                user.is_superuser=False
                user.is_staff=False
                user.is_active=False
                user.set_password(post_password)
                user.security_hash = "".join(random.sample(KEYS,24))
                user.save()
                #raise AssertionError(reverse('account_signup_confirm'))
                
                host = request.META['HTTP_HOST']
                subject = "Evesch Registration Confirmation"
                email_body = render_to_string("core/email_registration_confirmation.html", { 'username': user.username,
                                            'link': "http://" + host + reverse('account_signup_confirm') + "?registration_confirmation=" + user.security_hash,
                                             'registration_confirmation':user.security_hash,})
                email_from = ""
                email_recipients = post_email
                # Create a new thread in Daemon mode to send message
                t = threading.Thread(target=send_mail,
                                     args=[subject, email_body, email_from, email_recipients],
                                     kwargs={'fail_silently': True})
                t.setDaemon(True)
                t.start()

                return HttpResponseRedirect(reverse('account_signup_confirm'))
        else: 
            form = SignupForm(None)
        context = {'form':form,}
    return render_to_response(template_name,context,context_instance=RequestContext(request)) 


def evesch_signup_confirm(request, template_name=None):
    message = None

    security_hash_get = ""
    if request.GET.__contains__("registration_confirmation"): 
        security_hash_get = request.GET.get('registration_confirmation',"")

    #raise AssertionError(security_hash_get)
    if request.POST:
        form = SignupConfirmForm(request.POST)
        if form.is_valid():
            security_hash_post = form.cleaned_data['security_hash']

            try:
                user =  User.objects.get(security_hash=security_hash_post)
                if user.is_active == False: 
                    user.is_active = True
                    user.save()
                    return HttpResponseRedirect(reverse('account_auth_login'))
                else:
                    message = _("You have already confirmed your account.  Proceed to the login page.")          
            except:
                message = _("Incorrect registration key. Please refer to your email for the correct key.")

    else:
        form = SignupConfirmForm()
        form.initial = {'security_hash':security_hash_get,}
    context = {'form':form,'message':message}
    return render_to_response(template_name,context,context_instance=RequestContext(request)) 


def evesch_captcha(request):
    from random import choice
    import Image, ImageDraw, ImageFont, sha
    SALT = settings.SECRET_KEY[:20]
    imgtext = ''.join([choice('QWERTYUOPASDFGHJKLZXCVBNM') for i in range(5)])
    request.session['signup_captcha'] = imgtext

    imghash = sha.new(SALT+imgtext).hexdigest()
    im=Image.open(settings.MEDIA_ROOT + 'images/captcha_box.jpg')
    (bg_width, bg_height) = im.size
    draw=ImageDraw.Draw(im)
    font=ImageFont.truetype(settings.MEDIA_ROOT + 'fonts/Cracked', 44)
    (txt_width, txt_height) = draw.textsize(imgtext, font=font) 
    draw.text(((bg_width / 2 ) - (txt_width / 2), (bg_height / 2) - (txt_height / 2) ),imgtext, font=font, fill=(100,100,50))

    for i in range(5):
        x0 = random.randint(0, im.size[0])
        y0 = random.randint(0, im.size[1])
        x1 = random.randint(0, im.size[0])
        y1 = random.randint(0, im.size[1])
        draw.rectangle((x0, y0, x1, y1), outline=(100,100,50))

    response = HttpResponse(mimetype="image/png")
    im.save(response, "PNG")
    return response

def evesch_password_reset(request, template_name=None):
    if request.POST:
        session_captcha = request.session.get('signup_captcha', '-1')
        form = PasswordResetForm(session_captcha, request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            return HttpResponseRedirect(reverse('home'))
    else: 
        form = PasswordResetForm(None)
    context = {'form':form,}
    return render_to_response(template_name,context,context_instance=RequestContext(request)) 
 

def error(request,template_name):
    return render_to_response("error.html",{'error':_("Error")})

def page_not_found(request,template_name):
    return render_to_response(template_name,{'message':_("Page Not Found")},context_instance=RequestContext(request))
