from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.generic import TemplateView
from evesch.core.views import index, page_not_found


urlpatterns = []

if settings.DEBUG:

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += [
            url(r'^rosetta/', include('rosetta.urls')),
        ]

urlpatterns += [
    # Uncomment this for admin:
    url('^robots.txt$', TemplateView.as_view(template_name='robots.txt')),
    url('^$', index, {'template_name': "index.html"}, name='home'),
    url(r'^org/', include('evesch.org.urls')),
    url(r'^user/', include('evesch.euser.urls')),
    url(r'^accounts/', include('evesch.core.urls')),
    url(r'^ajax_filtered_fields/', include('evesch.core.ajax_filtered_fields.urls')),
    url('.*', page_not_found, {'template_name': "error.html"}, name='core_page_not_found'),
]
