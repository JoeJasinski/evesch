from django.conf.urls import url
from evesch.egroup import views

urlpatterns = [
    url(r'^add/$',
        views.group_add,
        {'template_name': 'egroup/group_add.html'},
        name='egroup_group_add'),
    url(r'^(?P<group_hash>\w{1,16})/$',
        views.group_view,
        {'template_name': 'egroup/group_view.html'},
        name='egroup_group_view'),
    url(r'^(?P<group_hash>\w{1,16})/ajax/members/$',
        views.group_members,
        {'template_name': 'egroup/ajax/ajax_group_user_list.html'},
        name='egroup_group_user_list_ajax'),
    url(r'^(?P<group_hash>\w{1,16})/edit/$',
        views.group_edit,
        {'template_name': 'egroup/group_edit.html'},
        name='egroup_group_edit'),
    url(r'^(?P<group_hash>\w{1,16})/remove/$',
        views.group_remove,
        {'template_name': 'egroup/group_remove.html'},
        name='egroup_group_remove'),
    url(r'^(?P<group_hash>\w{1,16})/remove/(?P<group_user>\w{1,30})/$',
        views.groupuser_remove,
        {'template_name': 'egroup/group_edit.html'},
        name='egroup_groupuser_remove'),
]
