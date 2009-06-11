from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )



urlpatterns += patterns('evesch',
    # Uncomment this for admin:
     (r'^admin/(.*)', admin.site.root),
     url('^$','core.views.index', {'template_name':"index.html"},name='home'),
     (r'^org/', include('org.urls')),
     (r'^user/', include('euser.urls')),
     (r'^accounts/', include('core.urls')),
     url('.*','core.views.page_not_found', {'template_name':"error.html"}, name='core_page_not_found'),
)
