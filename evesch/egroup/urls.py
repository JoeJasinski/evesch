from django.conf.urls.defaults import *
from event.views import *

urlpatterns = patterns('',  
     url('^add/$','egroup.views.group_add',{'template_name':'egroup/group_add.html'},name='egroup_group_add'),
     #url('^(?P<group_hash>\w{1,8})/$','egroup.views.group_view',{'template_name':'egroup/group_view.html'},name='egroup_group_view'),
     url('^(?P<group_hash>\w{1,16})/edit/$','egroup.views.group_edit',{'template_name':'egroup/group_edit.html'},name='egroup_group_edit'),
     url('^(?P<group_hash>\w{1,16})/remove/$','egroup.views.group_remove',{'template_name':'egroup/group_remove.html'},name='egroup_group_remove'),
)
