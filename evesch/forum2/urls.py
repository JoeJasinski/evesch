from django.conf.urls.defaults import *
from ecalendar.views import *

urlpatterns = patterns('',
    url('^$', 'forum.views.forum_list', {'template_name':"forum/forum_list.html"}, name='forum_forum_list' ),
)
