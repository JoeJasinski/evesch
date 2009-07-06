from django.conf.urls.defaults import *


urlpatterns = patterns('',                  
     url('^login/$','core.views.evesch_login',{'template_name':'core/login.html'},name='account_auth_login'),
     url('^logout/$','core.views.evesch_logout',{'template_name':'core/login.html'},name='account_auth_logout'),
     url('^signup/$','core.views.evesch_signup',{'template_name':'core/signup.html'},name='account_signup'),
     url('^signup/captcha.png$','core.views.evesch_captcha',{},name='account_signup_captcha'),
     url('^password_reset/$','core.views.evesch_password_reset',{'template_name':'core/password_reset.html'},name='account_password_reset')
)
