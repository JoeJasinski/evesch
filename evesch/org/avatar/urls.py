from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('org.avatar.views',
    url('^change/$', 'change', name='org_org_edit_photo'),
    url('^delete/$', 'delete', name='org_org_delete_photo'),
)
