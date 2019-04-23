from django.conf.urls import url
from forum import views

urlpatterns = [
    url(
        r'^$',
        views.forum_list,
        {'template_name': "forum/forum_list.html"},
        name='forum_forum_list'),
]
