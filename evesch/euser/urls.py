from django.conf.urls import  url
from evesch.euser import views
from evesch.core.feed import views as feed_views

urlpatterns = [
    url(r'^(?P<username>\w{1,30})/$',
        views.user_view,
        {'template_name': 'euser/user_view.html'},
        name='euser_user_view'),    
    url(r'^ajax/lookup_users/$',
        views.lookup_users,
        {'template_name': 'euser/ajax/lookup_users.html'},
        name='euser_ajax_lookup_users'),
    url(r'^ajax/lookup_org_users/(?P<org_short_name>[\w_-]{1,20})/$',
        views.lookup_users,
        {'template_name': 'euser/ajax/lookup_users.html'},
        name='euser_ajax_lookup_org_users'),
    url(r'^(?P<username>\w{1,30})/ical_(?P<user_feed_hash>\w{1,24}).ics$',
        feed_views.user_ics, {},
        name='core_feed_user_ics'),
    url(r'^(?P<username>\w{1,30})/feed_(?P<user_feed_hash>\w{1,24}).rss$',
        feed_views.user_rss, {},
        name='core_feed_user_rss'),
]
