from django.conf.urls import patterns, include, url


urlpatterns = patterns('',                  
    url('^login/$','evesch.core.views.evesch_login',{'template_name':'core/login.html'},name='account_auth_login'),
    url('^logout/$','evesch.core.views.evesch_logout',{'template_name':'core/login.html'},name='account_auth_logout'),
    url('^signup/$','evesch.core.views.evesch_signup',{'template_name':'core/signup.html'},name='account_signup'),
    url('^signup/confirm/','evesch.core.views.evesch_signup_confirm',{'template_name':'core/signup_confirm.html'},name='account_signup_confirm'),
    url('^signup/success/','evesch.core.views.evesch_signup_success',{'template_name':'core/signup_success.html'},name='account_signup_success'),
    url('^signup/captcha.png$','evesch.core.views.evesch_captcha',{},name='account_signup_captcha'),
    url('^password_reset/$','evesch.core.views.evesch_password_reset',{'template_name':'core/password_reset.html'},name='account_password_reset'),
    url('^password_reset/sent/$','evesch.core.views.evesch_password_reset_sent',{'template_name':'core/password_reset_sent.html'},name='account_password_reset_sent'),
    url('^settings/$', 'evesch.euser.views.user_settings', {'template_name':'euser/user_settings.html'}, name='euser_user_settings'), 
)
