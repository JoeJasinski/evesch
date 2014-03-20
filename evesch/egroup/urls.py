from django.conf.urls import patterns, include, url
from evesch.event.views import *

urlpatterns = patterns('',  
     url('^add/$','evesch.egroup.views.group_add',{'template_name':'egroup/group_add.html'},name='egroup_group_add'),
     url('^(?P<group_hash>\w{1,16})/$','evesch.egroup.views.group_view',{'template_name':'egroup/group_view.html'},name='egroup_group_view'),
     url('^(?P<group_hash>\w{1,16})/ajax/members/$', 'evesch.egroup.views.group_members', {'template_name':'egroup/ajax/ajax_group_user_list.html'}, name='egroup_group_user_list_ajax'),  
     url('^(?P<group_hash>\w{1,16})/edit/$','evesch.egroup.views.group_edit',{'template_name':'egroup/group_edit.html'},name='egroup_group_edit'),
     url('^(?P<group_hash>\w{1,16})/remove/$','evesch.egroup.views.group_remove',{'template_name':'egroup/group_remove.html'},name='egroup_group_remove'),     
     url('^(?P<group_hash>\w{1,16})/remove/(?P<group_user>\w{1,30})/$','evesch.egroup.views.groupuser_remove',{'template_name':'egroup/group_edit.html'},name='egroup_groupuser_remove'),     
)
