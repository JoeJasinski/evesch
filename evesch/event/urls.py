from django.conf.urls.defaults import *

urlpatterns = patterns('',  
     url('^event/add/$','event.views.event_add',{'template_name':'event/event_add.html'},name='event_event_add'),
     #url('^event/view/(?P<event_id>\w{1,10})/$','event.views.event_view',{'template_name':'error.html'},name='event_event_view'),
     url('^event/(?P<event_hash>\w{1,8})/$','event.views.event_view',{'template_name':'event/event_view.html'},name='event_event_view'),
     url('^event/(?P<event_hash>\w{1,8})/edit/$','event.views.event_edit',{'template_name':'event/event_edit.html'},name='event_event_edit'),
     url('^event/(?P<event_hash>\w{1,8})/remove/$','event.views.event_remove',{'template_name':'event/event_remove.html'},name='event_event_remove'),
     url('^event/(?P<event_hash>\w{1,8})/attendee/add/$','event.views.event_attendee_add',{'template_name':'event/event_attendee_add.html'},name='event_attendee_add'),
     url('^event/(?P<event_hash>\w{1,8})/attendee/(?P<att_name>\w{3,30})/remove/$','event.views.event_attendee_remove',{'template_name':'event/event_attendee_remove.html'}, name='event_attendee_remove'), 
     url('^event/(?P<event_hash>\w{1,8})/attendees/message/$','event.views.event_attendees_message',{'template_name':'core/message_users.html'}, name='event_attendees_message'),
     url('^events/$','event.views.events_list',{'template_name':'event/events_list.html'},name='event_events_list'),
     url('^eventtype/add/$','event.views.eventtype_add',{'template_name':'event/eventtype_add.html'},name='event_eventtype_add'),
     url('^eventtype/(?P<eventtype_hash>\w{1,8})/edit/$','event.views.eventtype_edit',{'template_name':'event/eventtype_edit.html'},name='event_eventtype_edit'),
     url('^eventtype/(?P<eventtype_hash>\w{1,8})/remove/$','event.views.eventtype_remove',{'template_name':'event/eventtype_remove.html'},name='event_eventtype_remove'),
)
