from django.conf.urls.defaults import *
from euser.views import *

urlpatterns = patterns('',
    url('^(?P<username>\w{1,30})/$', 'euser.views.user_view', {'template_name':'euser/user_view.html'}, name='euser_user_view'),    
    url('^ajax/lookup_users/$', 'euser.views.lookup_users', {'template_name':'euser/ajax/lookup_users.html'}, name='euser_ajax_lookup_users'),
    url('^ajax/lookup_org_users/(?P<org_short_name>[\w_-]{1,20})/$', 'euser.views.lookup_users', {'template_name':'euser/ajax/lookup_users.html'}, name='euser_ajax_lookup_org_users'),
    url('^(?P<username>\w{1,30})/ical_(?P<user_feed_hash>\w{1,24}).ics$', 'core.feed.views.user_ics', {}, name='core_feed_user_ics'),
    url('^(?P<username>\w{1,30})/feed_(?P<user_feed_hash>\w{1,24}).rss$', 'core.feed.views.user_rss', {}, name='core_feed_user_rss'),
)
