from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = patterns('',)

if settings.DEBUG:

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls')),
        )

urlpatterns += patterns('',
    # Uncomment this for admin:
     ('^robots.txt$',  TemplateView.as_view(template_name='robots.txt'), ),
     url('^$','evesch.core.views.index', {'template_name':"index.html"},name='home'),
     (r'^org/', include('evesch.org.urls')),
     (r'^user/', include('evesch.euser.urls')),
     (r'^accounts/', include('evesch.core.urls')),
     (r'^ajax_filtered_fields/', include('evesch.core.ajax_filtered_fields.urls')),
)
