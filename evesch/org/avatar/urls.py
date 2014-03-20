from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url('^change/$', 'evesch.org.avatar.views.change', name='org_org_edit_photo'),
    url('^delete/$', 'evesch.org.avatar.views.delete', name='org_org_delete_photo'),
)
