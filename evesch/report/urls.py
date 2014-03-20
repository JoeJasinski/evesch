from django.conf.urls import patterns, include, url
from evesch.euser.views import *

urlpatterns = patterns('',
     url('^$', 'evesch.report.views.org_reports', {'template_name':'report/org_report.html'}, name='report_org_reports'),  
     url('^by_user/$', 'evesch.report.views.org_reports', {'template_name':'report/org_report.html', 'type':'user'}, name='report_org_reports_by_user'), 
     url('^by_eventtype/$', 'evesch.report.views.org_reports', {'template_name':'report/org_report.html', 'type':'eventtype'}, name='report_org_reports_by_eventtype'), 
     url('^by_event/$', 'evesch.report.views.org_reports', {'template_name':'report/org_report.html', 'type':'event'}, name='report_org_reports_by_event'), 
)
