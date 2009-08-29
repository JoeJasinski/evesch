from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

    if 'core.rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls')),
        )

urlpatterns += patterns('evesch',
    # Uncomment this for admin:
     ('^robots.txt$', direct_to_template, {'template': 'robots.txt' }),
     (r'^admin/(.*)', admin.site.root),
     url('^$','core.views.index', {'template_name':"index.html"},name='home'),
     (r'^org/', include('org.urls')),
     (r'^user/', include('euser.urls')),
     (r'^accounts/', include('core.urls')),
     (r'^ajax_filtered_fields/', include('core.ajax_filtered_fields.urls')),
     url('.*','core.views.page_not_found', {'template_name':"error.html"}, name='core_page_not_found'),
)
