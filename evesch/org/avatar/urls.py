from django.conf.urls import url
from evesch.org.avatar.views import change, delete

urlpatterns = [
    url('^change/$', change, name='org_org_edit_photo'),
    url('^delete/$', delete, name='org_org_delete_photo'),
]
