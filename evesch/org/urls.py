# org/urls.py
# included by main_urls.py
from django.conf.urls.defaults import *
from org.views import *

urlpatterns = patterns('',
     url('^$', 'org.views.orgs_list', {'template_name':'org/orgs_list.html'}, name='org_orgs_list'),
     url('^ajax/$', 'org.views.orgs_list', {'template_name':'org/ajax/ajax_orgs_list_all_entry.html'}, name='org_orgs_list_ajax'),
     url('^ajax/all_orgs/$', 'org.views.orgs_list_all', {'template_name':'org/ajax/ajax_orgs_list_all_entry.html'}, name='org_orgs_list_all_ajax'),    
     url('^ajax/my_orgs/$', 'org.views.orgs_list_my', {'template_name':'org/ajax/ajax_orgs_list_my_entry.html'}, name='org_orgs_list_my_ajax'),     
     url('^(?P<org_short_name>[\w_-]{1,20})/ajax/members/$', 'org.views.org_members', {'template_name':'org/ajax/ajax_org_user_list.html'}, name='org_org_user_list_ajax'),    
     url('^(?P<org_short_name>[\w_-]{1,20})/ajax/invites/$', 'org.views.org_list_invites', {'template_name':'org/ajax/ajax_org_user_list.html'}, name='org_org_invites_list_ajax'), 
     url('^add/$', 'org.views.org_add', {'template_name':'org/org_add.html'}, name='org_org_add'), 
     url('^browse/$', 'org.views.org_browse', {'template_name':'org/org_browse.html'}, name='org_org_browse'), 
     url('^browse/(?P<filter_abc>)[a-z]{1}/$', 'org.views.org_browse', {'template_name':'org/org_browse.html'}, name='org_org_browse_filter_abc'), 
     (r'^(?P<org_short_name>[\w_-]{1,20})/photo/', include('org.avatar.urls')),
     url('^(?P<org_short_name>[\w_-]{1,20})/edit/$', 'org.views.org_edit', {'template_name':'org/org_edit.html'}, name='org_org_edit'), 
     url('^(?P<org_short_name>[\w_-]{1,20})/remove/$', 'org.views.org_remove', {'template_name':'org/org_remove.html'}, name='org_org_remove'),
     url('^(?P<org_short_name>[\w_-]{1,20})/join/$', 'org.views.org_join', {'template_name':'org/org_join.html'}, name='org_org_join'),
     url('^(?P<org_short_name>[\w_-]{1,20})/leave/$', 'org.views.org_leave', {'template_name':'org/org_leave.html'}, name='org_org_leave'),   
     url('^(?P<org_short_name>[\w_-]{1,20})/member/remove/(?P<username>\w{1,30})/','org.views.org_member_remove',{'template_name':'org/org_member_remove.html',}, name='org_org_member_remove'),      
     (r'^(?P<org_short_name>[\w_-]{1,20})/', include('event.urls')),
     (r'^(?P<org_short_name>[\w_-]{1,20})/group/', include('egroup.urls')),
     url('^(?P<org_short_name>[\w_-]{1,20})/$','org.views.org_view', {'template_name':'org/org_view.html'}, name='org_org_view'),
     url('^(?P<org_short_name>[\w_-]{1,20})/invite/$','org.views.org_member_invite', {'template_name':'org/org_member_invite.html'}, name='org_org_member_invite'),
     #(r'^(?P<org_short_name>[\w_-]{1,20})/forum/$',include('forum.urls')),     
     (r'^(?P<org_short_name>[\w_-]{1,20})/calendar/', include('ecalendar.urls')),
     (r'^(?P<org_short_name>[\w_-]{1,20})/reports/', include('report.urls')),    
     url('^(?P<org_short_name>[\w_-]{1,20})/feed_(?P<org_feed_hash>\w{1,20}).rss$', 'core.feed.views.org_rss', {}, name='core_feed_org_rss'),
     url('^(?P<org_short_name>[\w_-]{1,20})/ical_(?P<org_feed_hash>\w{1,20}).ics$', 'core.feed.views.org_ics', {}, name='core_feed_org_ics'),
)
